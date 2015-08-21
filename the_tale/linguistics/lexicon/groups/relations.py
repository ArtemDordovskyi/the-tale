# coding: utf-8

from rels import Column
from rels.django import DjangoEnum

from the_tale.linguistics.lexicon.relations import VARIABLE as V


class LEXICON_GROUP(DjangoEnum):
    index_group = Column()
    description = Column(unique=False)
    variables = Column(unique=False, no_index=True)

    records = (('ACTION_BATTLEPVE1X1', 0, u'Действие: сражение с монстром', 0,
               u'Описание событий, происходящих при сражении с монстрами.',
               {V.HERO: u'герой', V.ACTOR: u'герой или монстр', V.DAMAGE: u'количество урона', V.EXPERIENCE: u'опыт', V.ARTIFACT: u'предмет', V.MOB: u'монстр', V.COMPANION: u'спутник'}),

               ('ACTION_EQUIPPING', 1, u'Действие: экипировка', 10000,
               u'Описание событий во время изменения экипировки героя.',
               {V.UNEQUIPPED: u'снимаемый артефакт', V.ITEM: u'артефакт', V.HERO: u'герой', V.EQUIPPED: u'экипируемый артефакт'}),

               ('ACTION_EVENT', 2, u'Небольшие события', 20000,
               u'Описания небольших событий во время действий героя.',
               {V.PLACE: u'город', V.COINS: u'количество монет', V.HERO: u'герой', V.EXPERIENCE: u'опыт', V.ARTIFACT: u'артефакт'}),

               ('ACTION_IDLENESS', 3, u'Действие: бездействие героя', 30000,
               u'Описание моментов, когда герой ничего не делает.',
               {V.HERO: u'герой'}),

               ('ACTION_INPLACE', 4, u'Действие: посещение города', 40000,
               u'Описание событий, происходящих при посещении героем города.',
               {V.HERO: u'герой', V.COINS_DELTA: u'доплата', V.COINS: u'количество монет', V.ARTIFACT: u'предмет', V.SELL_PRICE: u'цена продажи', V.PERSON: u'житель', V.PLACE: u'город', V.EXPERIENCE: u'количество опыта', V.OLD_ARTIFACT: u'старый артефакт', V.COMPANION: u'спутник', V.HEALTH: u'количество здоровья'}),

               ('ACTION_MOVENEARPLACE', 5, u'Действие: путешествие в окрестностях города', 50000,
               u'Описание действий, происходящих при путешествии героя в окрестностях города.',
               {V.PLACE: u'город', V.HERO: u'герой'}),

               ('ACTION_MOVETO', 6, u'Действие: путешествие между городами', 60000,
               u'Описание событий при путешествии героя между городами (по дороге)',
               {V.DESTINATION: u'конечное место назначения', V.HERO: u'герой', V.CURRENT_DESTINATION: u'текущее место назначения'}),

               ('ACTION_QUEST', 7, u'Действие: выполнение задания', 70000,
               u'Герой выполняет специфические для задания действия.',
               {V.HERO: u'герой'}),

               ('ACTION_REGENERATE_ENERGY', 8, u'Действие: восстановление энергии', 80000,
               u'Описание событий во время проведения героем религиозных обрядов.',
               {V.ENERGY: u'количество энергии', V.HERO: u'герой'}),

               ('ACTION_REST', 9, u'Действие: лечение', 90000,
               u'Описание действий во время лечения героя.',
               {V.HEALTH: u'количество здоровья', V.HERO: u'герой'}),

               ('ACTION_RESURRECT', 10, u'Действие: воскрешение героя', 100000,
               u'Описание событий при воскрешении героя',
               {V.HERO: u'герой'}),

               ('ACTION_TRADING', 11, u'Действие: торговля', 110000,
               u'Описание действий во время торговли',
               {V.COINS: u'количество монет', V.HERO: u'герой', V.ARTIFACT: u'предмет'}),

               ('ANGEL_ABILITY', 12, u'Способности: Хранитель', 120000,
               u'Описание результата использование способностей игрока',
               {V.HERO: u'герой', V.DROPPED_ITEM: u'выкидываемый предмет', V.ENERGY: u'энергия', V.COINS: u'количество монет', V.EXPERIENCE: u'количество опыта', V.HEALTH: u'количество здоровья', V.MOB: u'монстр', V.COMPANION: u'спутник'}),

               ('CHRONICLE', 13, u'Летопись', 130000,
               u'Фразы, употребляющиеся в летописи.',
               {V.NEW_NAME: u'новое название', V.NEW_RACE: u'новая раса города', V.DECLINED_BILL: u'название отменяемого закона', V.PERSON: u'житель города', V.RESOURCE_2: u'второй ресурс', V.RESOURCE_1: u'первый ресурс', V.BILL: u'название закона', V.PLACE_2: u'второй город ', V.PLACE_1: u'первый город', V.PLACE: u'название города', V.OLD_NAME: u'старое название', V.OLD_RACE: u'старая раса города', V.NEW_MODIFIER: u'новая специализация города', V.OLD_MODIFIER: u'старая специализация города', V.CONVERSION: u'информация о конверсии параметров'}),

               ('HERO_ABILITY', 14, u'Способности', 140000,
               u'Описание применения способностей героем (или монстром)',
               {V.ATTACKER: u'атакующий', V.HEALTH: u'количество вылеченного здоровья', V.DAMAGE: u'количество урона', V.ATTACKER_DAMAGE: u'количество урона по атакующему', V.ACTOR: u'герой или монстр', V.DEFENDER: u'защищающийся', V.COMPANION: u'спутник'}),

               ('HERO_COMMON', 15, u'Общие сообщения, относящиеся к герою', 150000,
               u'Сообщение, относящиеся к герою и не вошедшие в другие модули',
               {V.HERO: u'герой', V.LEVEL: u'уровень', V.ARTIFACT: u'артефакт'}),

               ('META_ACTION_ARENA_PVP_1X1', 16, u'Действие: дуэль на арене', 160000,
               u'Описание действий во время PvP дуэли на арене',
               {V.DUELIST_2: u'2-ой участник дуэли', V.DUELIST_1: u'1-ый участник дуэли', V.KILLER: u'победитель', V.ATTACKER: u'атакующий', V.VICTIM: u'проигравший'}),

               ('PVP', 17, u'PvP: фразы', 170000,
               u'Фразы, употребляющиеся при PvP.',
               {V.TEXT: u'любой текст', V.EFFECTIVENESS: u'изменение эффективности', V.DUELIST_2: u'2-ой участник дуэли', V.DUELIST_1: u'1-ый участник дуэли'}),

               ('QUEST_CARAVAN', 18, u'Задание: провести караван', 180000,
               u'Тексты, относящиеся к заданию.',
               {V.INITIATOR: u'житель, начинающий задание', V.HERO: u'герой', V.ANTAGONIST_POSITION: u'место продажи награбленного', V.COINS: u'количество монет', V.ARTIFACT: u'артефакт', V.INITIATOR_POSITION: u'место начала задания', V.RECEIVER: u'житель, заканчивающий задание', V.RECEIVER_POSITION: u'место окончания задания'}),

               ('QUEST_COLLECT_DEBT', 19, u'Задание: чужие обязательства', 190000,
               u'Тексты, относящиеся к заданию.',
               {V.INITIATOR: u'житель, начинающий задание', V.HERO: u'герой', V.COINS: u'количество монет', V.ARTIFACT: u'артефакт', V.INITIATOR_POSITION: u'место начала задания', V.RECEIVER: u'житель, заканчивающий задание', V.RECEIVER_POSITION: u'место окончания задания'}),

               ('QUEST_DELIVERY', 20, u'Задание доставить письмо', 200000,
               u'Тексты, относящиеся к заданию',
               {V.INITIATOR: u'житель, начинающий задание', V.HERO: u'герой', V.ANTAGONIST_POSITION: u'место скупки краденого', V.COINS: u'количество монет', V.ARTIFACT: u'артефакт', V.INITIATOR_POSITION: u'место начала задания', V.RECEIVER: u'житель, заканчивающий задание', V.RECEIVER_POSITION: u'место окончания задания', V.ANTAGONIST: u'житель, скупающий краденое'}),

               ('QUEST_HELP', 21, u'Задание: помощь', 210000,
               u'Тексты, относящиеся к заданию.',
               {V.INITIATOR: u'житель, начинающий задание', V.HERO: u'герой', V.COINS: u'количество монет', V.ARTIFACT: u'артефакт', V.INITIATOR_POSITION: u'место начала задания', V.RECEIVER: u'житель, заканчивающий задание', V.RECEIVER_POSITION: u'место окончания задания'}),

               ('QUEST_HELP_FRIEND', 22, u'Задание: помощь соратнику', 220000,
               u'Тексты, относящиеся к заданию.',
               {V.RECEIVER_POSITION: u'место окончания задания', V.COINS: u'количество монет', V.HERO: u'герой', V.ARTIFACT: u'артефакт', V.RECEIVER: u'житель, заканчивающий задание'}),

               ('QUEST_HOMETOWN', 23, u'Задание: путешествие в родной город', 230000,
               u'Тексты, относящиеся к заданию.',
               {V.RECEIVER_POSITION: u'место окончания задания', V.COINS: u'количество монет', V.HERO: u'герой', V.INITIATOR_POSITION: u'место начала задания', V.ARTIFACT: u'артефакт'}),

               ('QUEST_HUNT', 24, u'Задание: охота', 240000,
               u'Тексты, относящиеся к заданию.',
               {V.RECEIVER_POSITION: u'место окончания задания', V.COINS: u'количество монет', V.HERO: u'герой', V.ARTIFACT: u'артефакт'}),

               ('QUEST_INTERFERE_ENEMY', 25, u'Задание: навредить противнику', 250000,
               u'Тексты, относящиеся к заданию.',
               {V.HERO: u'герой', V.ANTAGONIST_POSITION: u'место деятельности противника', V.COINS: u'количество монет', V.ARTIFACT: u'артефакт', V.RECEIVER: u'противник', V.RECEIVER_POSITION: u'место жительства противника'}),

               ('QUEST_PILGRIMAGE', 26, u'Задание: паломничество в святой город', 260000,
               u'Тексты, относящиеся к заданию.',
               {V.RECEIVER_POSITION: u'место окончания задания', V.COINS: u'количество монет', V.HERO: u'герой', V.INITIATOR_POSITION: u'место начала задания', V.ARTIFACT: u'артефакт'}),

               ('QUEST_SEARCH_SMITH', 27, u'Задание: посещение кузнеца', 270000,
               u'Тексты, относящиеся к заданию.',
               {V.UNEQUIPPED: u'снимаемый артефакт', V.HERO: u'герой', V.COINS: u'цена работы кузнеца', V.ARTIFACT: u'артефакт', V.SELL_PRICE: u'цена продажи', V.RECEIVER: u'житель, заканчивающий задание', V.RECEIVER_POSITION: u'место окончания задания'}),

               ('QUEST_SPYING', 28, u'Задание: шпионаж', 280000,
               u'Тексты, относящиеся к заданию.',
               {V.INITIATOR: u'житель, начинающий задание', V.HERO: u'герой', V.COINS: u'количество монет', V.ARTIFACT: u'артефакт', V.INITIATOR_POSITION: u'место начала задания', V.RECEIVER: u'житель, заканчивающий задание', V.RECEIVER_POSITION: u'место окончания задания'}),

               ('COMPANIONS', 29, u'Спутники', 290000,
               u'Тексты, относящиеся к спутникам.',
               {V.COMPANION_OWNER: u'владелец спутника', V.COMPANION: u'спутник', V.ATTACKER: u'атакущий спутника', V.COINS: u'вырученные средства', V.EXPERIENCE: u'опыт', V.HEALTH: u'количество здоровья', V.MOB: u'монстр', V.DESTINATION: u'место назначения'}),

               ('ACTION_HEAL_COMPANION', 30, u'Действие: уход за спутником', 300000,
               u'Герой ухаживает за спутником (обрабатывает раны, смазывает детальки, чистит карму, в зависимости от спутника).',
               {V.HERO: u'герой', V.COMPANION: u'спутник', V.HEALTH: u'количество здоровья'}),
               )
