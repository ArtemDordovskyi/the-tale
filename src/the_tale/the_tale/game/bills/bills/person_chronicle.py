
from dext.forms import fields

from the_tale.game.persons import objects as persons_objects
from the_tale.game.persons import storage as persons_storage
from the_tale.game.persons import logic as persons_logic

from the_tale.game.politic_power import logic as politic_power_logic

from the_tale.game import tt_api_impacts

from the_tale.game.bills import relations
from the_tale.game.bills.forms import BaseUserForm, ModeratorFormMixin
from the_tale.game.bills.bills.base_person_bill import BasePersonBill


class BaseForm(BaseUserForm):
    person = fields.ChoiceField(label='Мастер')
    power_bonus = fields.RelationField(label='Изменение влияния', relation=relations.POWER_BONUS_CHANGES)

    def __init__(self, choosen_person_id, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.fields['person'].choices = persons_objects.Person.form_choices(choosen_person=persons_storage.persons.get(choosen_person_id))


class UserForm(BaseForm):
    pass


class ModeratorForm(BaseForm, ModeratorFormMixin):
    pass


class PersonChronicle(BasePersonBill):
    type = relations.BILL_TYPE.PERSON_CHRONICLE

    UserForm = UserForm
    ModeratorForm = ModeratorForm

    CAPTION = 'Запись в летописи о Мастере'
    DESCRIPTION = 'В жизни происходит множество интересных событий. Часть из них оказывается достойна занесения в летопись и может немного повлиять на влиятельность участвующего в них Мастера.'

    def __init__(self, power_bonus=None, **kwargs):
        super(PersonChronicle, self).__init__(**kwargs)
        self.power_bonus = power_bonus

    def has_meaning(self):
        return self.person

    def apply(self, bill=None):
        if not self.has_meaning():
            return

        if self.power_bonus.bonus == 0:
            return

        impacts = list(persons_logic.tt_power_impacts(person_inner_circle=False,
                                                      place_inner_circle=False,
                                                      actor_type=tt_api_impacts.OBJECT_TYPE.BILL,
                                                      actor_id=bill.id,
                                                      person=self.person,
                                                      amount=self.power_bonus.bonus,
                                                      fame=0))

        politic_power_logic.add_power_impacts(impacts)

    def user_form_initials(self):
        initials = super(PersonChronicle, self).user_form_initials()
        initials['power_bonus'] = self.power_bonus
        return initials

    def initialize_with_form(self, user_form):
        super(PersonChronicle, self).initialize_with_form(user_form)
        self.power_bonus = user_form.c.power_bonus

    def serialize(self):
        data = super(PersonChronicle, self).serialize()
        data['power_bonus'] = self.power_bonus.value
        return data

    @classmethod
    def deserialize(cls, data):
        obj = super(PersonChronicle, cls).deserialize(data)
        obj.power_bonus = relations.POWER_BONUS_CHANGES(data['power_bonus'])
        return obj
