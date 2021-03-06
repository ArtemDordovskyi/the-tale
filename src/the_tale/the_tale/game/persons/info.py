
import time

from the_tale.game.chronicle import prototypes as chronicle_prototypes

from the_tale.game import attributes
from the_tale.game import logic as game_logic

from the_tale.game.politic_power import logic as politic_power_logic
from the_tale.game.politic_power import storage as politic_power_storage

from the_tale.game.places import info as places_info
from the_tale.game.places import storage as places_storage

from . import conf
from . import relations


def person_info(person):
    building = places_storage.buildings.get_by_person_id(person.id)

    inner_circle = politic_power_logic.get_inner_circle(person_id=person.id)

    data = {'id': person.id,
            'name': person.name,
            'updated_at': time.mktime(person.updated_at.timetuple()),

            'profession': person.type.value,
            'race': person.race.value,
            'gender': person.gender.value,

            'place': {
                'id': person.place.id,
                'name': person.place.name,
                'size': person.place.attrs.size,
                'specialization': person.place.modifier.value,
                'position': {'x': person.place.x, 'y': person.place.y}
            },

            'building': places_info.building_info(building) if building else None,
            'politic_power': {'heroes': inner_circle.ui_info(),
                              'power': politic_power_storage.persons.ui_info(person.id)},
            'attributes': attributes.attributes_info(effects=person.all_effects(),
                                                     attrs=person.attrs,
                                                     relation=relations.ATTRIBUTE),
            'chronicle': chronicle_prototypes.chronicle_info(person, conf.settings.CHRONICLE_RECORDS_NUMBER),
            'job': person.job.ui_info(),
            'accounts': None,
            'clans': None}

    accounts_ids = set()
    accounts_ids.update(data['politic_power']['heroes']['positive'])
    accounts_ids.update(data['politic_power']['heroes']['negative'])

    data['accounts'] = game_logic.accounts_info(accounts_ids)
    data['clans'] = game_logic.clans_info(data['accounts'])

    return data
