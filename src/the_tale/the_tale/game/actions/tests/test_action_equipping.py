
from the_tale.common.utils import testcase

from the_tale.game.balance.power import Power

from the_tale.game.logic_storage import LogicStorage
from the_tale.game.logic import create_test_map

from the_tale.game.actions.prototypes import ActionEquippingPrototype

from the_tale.game.artifacts import storage as artifacts_storage
from the_tale.game.artifacts import relations as artifacts_relations

from the_tale.game import turn


class ActionEquippingTest(testcase.TestCase):

    def setUp(self):
        super(ActionEquippingTest, self).setUp()

        create_test_map()

        account = self.accounts_factory.create_account(is_fast=True)

        self.storage = LogicStorage()
        self.storage.load_account_data(account)
        self.hero = self.storage.accounts_to_heroes[account.id]
        self.action_idl = self.hero.actions.current_action

        self.action_equipping = ActionEquippingPrototype.create(hero=self.hero)


    def tearDown(self):
        pass


    def test_create(self):
        self.assertEqual(self.action_idl.leader, False)
        self.assertEqual(self.action_equipping.leader, True)
        self.assertEqual(self.action_equipping.bundle_id, self.action_idl.bundle_id)
        self.storage._test_save()


    def test_processed(self):
        self.storage.process_turn(continue_steps_if_needed=False)
        self.assertEqual(len(self.hero.actions.actions_list), 1)
        self.assertEqual(self.hero.actions.current_action, self.action_idl)
        self.storage._test_save()


    def test_equip(self):
        artifact = artifacts_storage.artifacts.generate_artifact_from_list(artifacts_storage.artifacts.artifacts, self.hero.level, rarity=artifacts_relations.RARITY.NORMAL)
        artifact.power = Power(666, 666)

        equip_slot = artifact.type.equipment_slot
        self.hero.equipment.unequip(equip_slot)

        self.hero.bag.put_artifact(artifact)

        self.storage.process_turn()
        self.assertEqual(len(self.hero.actions.actions_list), 2)
        self.assertEqual(self.hero.actions.current_action, self.action_equipping)
        self.assertEqual(len(list(self.hero.bag.items())), 0)

        equip_slot = artifact.type.equipment_slot
        self.assertEqual(self.hero.equipment.get(equip_slot), artifact)

        self.storage._test_save()

    def test_switch_artifact(self):
        artifact = artifacts_storage.artifacts.generate_artifact_from_list(artifacts_storage.artifacts.artifacts, self.hero.level, rarity=artifacts_relations.RARITY.NORMAL)
        artifact.power = Power(13, 13)

        equip_slot = artifact.type.equipment_slot

        self.hero.equipment.unequip(equip_slot)
        self.hero.equipment.equip(equip_slot, artifact)

        new_artifact = artifacts_storage.artifacts.generate_artifact_from_list([artifact.record], self.hero.level+1, rarity=artifacts_relations.RARITY.NORMAL)
        new_artifact.power = Power(666, 666)

        self.hero.bag.put_artifact(new_artifact)

        self.storage.process_turn()

        self.assertEqual(len(self.hero.actions.actions_list), 2)
        self.assertEqual(self.hero.actions.current_action, self.action_equipping)

        self.assertEqual(len(list(self.hero.bag.items())), 1)
        self.assertEqual(list(self.hero.bag.items())[0][1].power, Power(13, 13))

        equip_slot = artifact.type.equipment_slot

        self.assertEqual(self.hero.equipment.get(equip_slot), new_artifact)
        self.assertEqual(self.hero.equipment.get(equip_slot).power, Power(666, 666))

        turn.increment()

        self.storage.process_turn(continue_steps_if_needed=False)
        self.assertEqual(len(self.hero.actions.actions_list), 1)
        self.assertEqual(self.hero.actions.current_action, self.action_idl)

        self.storage._test_save()
