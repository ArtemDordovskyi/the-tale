
import time
import math
import datetime

from django.conf import settings as project_settings
from django.contrib.auth import login as django_login, authenticate as django_authenticate, logout as django_logout
from django.db import transaction

from dext.common.utils.logic import normalize_email
from dext.common.utils.urls import url

from the_tale import amqp_environment

from the_tale.common.utils.password import generate_password

from the_tale.game import relations as game_relations

from the_tale.accounts.models import Account
from the_tale.accounts.prototypes import AccountPrototype
from the_tale.accounts import exceptions
from the_tale.accounts.conf import accounts_settings

from the_tale.accounts.achievements.prototypes import AccountAchievementsPrototype

from the_tale.collections.prototypes import AccountItemsPrototype

from . import conf
from . import tt_api
from . import signals


class REGISTER_USER_RESULT:
    OK = 0
    DUPLICATE_USERNAME = 1
    DUPLICATE_EMAIL = 2


def login_url(target_url='/'):
    return url('accounts:auth:api-login', api_version='1.0', api_client=project_settings.API_CLIENT, next_url=target_url.encode('utf-8'))


def login_page_url(target_url='/'):
    return url('accounts:auth:page-login', next_url=target_url.encode('utf-8'))


def logout_url():
    return url('accounts:auth:api-logout', api_version='1.0', api_client=project_settings.API_CLIENT)


def get_system_user_id():
    if not project_settings.TESTS_RUNNING and hasattr(get_system_user_id, '_id'):
        return get_system_user_id._id

    account = get_system_user()

    get_system_user_id._id = account.id

    return get_system_user_id._id


def get_system_user():
    account = AccountPrototype.get_by_nick(accounts_settings.SYSTEM_USER_NICK)

    if account:
        return account

    register_result, account_id, bundle_id = register_user(accounts_settings.SYSTEM_USER_NICK, # pylint: disable=W0612
                                                           email=project_settings.EMAIL_NOREPLY,
                                                           password=generate_password(len_=accounts_settings.RESET_PASSWORD_LENGTH))

    account = AccountPrototype.get_by_id(account_id)
    account._model.active_end_at = datetime.datetime.fromtimestamp(0)
    account.save()

    return account


def register_user(nick,
                  email=None,
                  password=None,
                  referer=None,
                  referral_of_id=None,
                  action_id=None,
                  is_bot=False,
                  gender=game_relations.GENDER.MALE,
                  full_create=True):
    from the_tale.game import tt_api_energy
    from the_tale.game.heroes import logic as heroes_logic
    from the_tale.game.balance import constants as c

    if Account.objects.filter(nick=nick).exists():
        return REGISTER_USER_RESULT.DUPLICATE_USERNAME, None, None

    if email and Account.objects.filter(email=email).exists():
        return REGISTER_USER_RESULT.DUPLICATE_EMAIL, None, None

    try:
        referral_of = AccountPrototype.get_by_id(referral_of_id)
    except ValueError:
        referral_of = None

    if (email and not password) or (not email and password):
        raise exceptions.EmailAndPasswordError()

    is_fast = not (email and password)

    if is_fast and is_bot:
        raise exceptions.BotIsFastError()

    if password is None:
        password = accounts_settings.FAST_REGISTRATION_USER_PASSWORD

    account = AccountPrototype.create(nick=nick,
                                      email=email,
                                      is_fast=is_fast,
                                      is_bot=is_bot,
                                      password=password,
                                      referer=referer,
                                      referral_of=referral_of,
                                      action_id=action_id,
                                      gender=gender)

    AccountAchievementsPrototype.create(account)
    AccountItemsPrototype.create(account)

    hero = heroes_logic.create_hero(account=account, full_create=full_create)

    if full_create:
        tt_api_energy.change_energy_balance(account_id=account.id,
                                            type='initial_contribution',
                                            energy=c.INITIAL_ENERGY_AMOUNT,
                                            async=False,
                                            autocommit=True)

        tt_api.create_cards_timer(account_id=account.id)

    return REGISTER_USER_RESULT.OK, account.id, hero.actions.current_action.bundle_id


def login_user(request, nick=None, password=None, remember=False):
    user = django_authenticate(nick=nick, password=password)

    if request.user.id != user.id:
        request.session.flush()

    django_login(request, user)

    if remember:
        request.session.set_expiry(accounts_settings.SESSION_REMEMBER_TIME)


def force_login_user(request, user):

    if request.user.id != user.id:
        request.session.flush()

    user.backend = project_settings.AUTHENTICATION_BACKENDS[0]

    django_login(request, user)



def logout_user(request):
    signals.on_before_logout.send(None, request=request)

    django_logout(request)
    request.session.flush()

    request.session[accounts_settings.SESSION_FIRST_TIME_VISIT_VISITED_KEY] = True


def remove_account(account, force=False):
    from the_tale.game.logic import remove_game_data
    if force or account.can_be_removed():
        with transaction.atomic():
            remove_game_data(account)
            account.remove()


def block_expired_accounts():

    expired_before = datetime.datetime.now() - datetime.timedelta(seconds=accounts_settings.FAST_ACCOUNT_EXPIRED_TIME)

    for account_model in Account.objects.filter(is_fast=True, created_at__lt=expired_before):
        remove_account(AccountPrototype(account_model))


def thin_out_accounts(number, prolong_active_to):
    from . import models

    from the_tale.game.bills import models as bills_models
    from the_tale.blogs import models as blogs_models
    from the_tale.forum import models as forum_models

    restricted_accounts = set()
    restricted_accounts |= set(models.RandomPremiumRequest.objects.values_list('initiator', flat=True))
    restricted_accounts |= set(models.RandomPremiumRequest.objects.values_list('receiver', flat=True))
    restricted_accounts |= set(Account.objects.exclude(clan_id=None).values_list('id', flat=True))
    restricted_accounts |= set(bills_models.Bill.objects.values_list('owner_id', flat=True))
    restricted_accounts |= set(blogs_models.Post.objects.values_list('author_id', flat=True))
    restricted_accounts |= set(blogs_models.Post.objects.values_list('moderator_id', flat=True))
    restricted_accounts |= set(forum_models.Post.objects.values_list('author_id', flat=True))
    restricted_accounts |= set(forum_models.Thread.objects.values_list('author_id', flat=True))

    for account_model in Account.objects.all().order_by('created_at')[number:]:
        if account_model.id not in restricted_accounts:
            remove_account(AccountPrototype(account_model), force=True)

    Account.objects.all().update(active_end_at=datetime.datetime.now() + datetime.timedelta(seconds=prolong_active_to))


# for bank
def get_account_id_by_email(email):
    account = AccountPrototype.get_by_email(normalize_email(email))
    return account.id if account else None


def get_session_expire_at_timestamp(request):
    return time.mktime(request.session.get_expiry_date().timetuple())


def is_first_time_visit(request):
    return not request.user.is_authenticated and request.session.get(accounts_settings.SESSION_FIRST_TIME_VISIT_KEY)


def get_account_info(account, hero):
    from the_tale.game.ratings import prototypes as ratings_prototypes
    from the_tale.game.ratings import relations as ratings_relations
    from the_tale.game.places import storage as places_storage
    from the_tale.game.places import logic as places_logic

    ratings = {}

    rating_places = ratings_prototypes.RatingPlacesPrototype.get_by_account_id(account.id)

    rating_values = ratings_prototypes.RatingValuesPrototype.get_by_account_id(account.id)

    if rating_values and rating_places:
        for rating in ratings_relations.RATING_TYPE.records:
            ratings[rating.value] = {'name': rating.text,
                                     'place': getattr(rating_places, '%s_place' % rating.field, None),
                                     'value': getattr(rating_values, rating.field, None)}

    popularity = places_logic.get_hero_popularity(hero.id)

    places_history = [{'place': {'id': place_id,
                                 'name': places_storage.places[place_id].name},
                       'count': help_count} for place_id, help_count in popularity.places_rating()]

    clan_info = None

    if account.clan_id:
        clan = account.clan
        clan_info = {'id': clan.id,
                     'abbr': clan.abbr,
                     'name': clan.name}

    return {'id': account.id,
            'registered': not account.is_fast,
            'name': account.nick_verbose,
            'hero_id': hero.id,
            'places_history': places_history,
            'might': account.might,
            'achievements': AccountAchievementsPrototype.get_by_account_id(account.id).points,
            'collections': AccountItemsPrototype.get_by_account_id(account.id).get_items_count(),
            'referrals': account.referrals_number,
            'ratings': ratings,
            'permissions': {
                'can_affect_game': account.can_affect_game
                },
            'description': account.description_html,
            'clan': clan_info}


def get_transfer_commission(money):
    commission = int(math.floor(money * conf.accounts_settings.MONEY_SEND_COMMISSION))

    if commission == 0:
        commission = 1

    return commission


def initiate_transfer_money(sender_id, recipient_id, amount, comment):
    from the_tale.common.postponed_tasks.prototypes import PostponedTaskPrototype
    from the_tale.accounts import postponed_tasks

    commission = get_transfer_commission(amount)

    task = postponed_tasks.TransferMoneyTask(sender_id=sender_id,
                                             recipient_id=recipient_id,
                                             amount=amount-commission,
                                             commission=commission,
                                             comment=comment)
    task = PostponedTaskPrototype.create(task)

    amqp_environment.environment.workers.refrigerator.cmd_wait_task(task.id)

    return task
