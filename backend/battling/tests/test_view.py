from django.urls import reverse

from model_bakery import baker

from battling.models import Battle
from common.utils.tests import TestCaseUtils


class CreateBattleViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.opponent2 = baker.make("users.User")

    def test_create_battle_with_user_not_logged(self):
        self.auth_client.logout()
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        self.auth_client.post(reverse("create_battle"), battle_data)
        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)

        self.assertFalse(battle)

    def test_create_one_battle(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        self.auth_client.login(username=self.user.email, password="admin")
        self.auth_client.post(reverse("create_battle"), battle_data)
        battle = Battle.objects.get(creator=self.user, opponent=self.opponent)

        self.assertCountEqual(battle.creator.email, self.user.email)
        self.assertCountEqual(battle.opponent.email, self.opponent.email)

    def test_create_battle_with_multiple_requests(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        battle2_data = {
            "creator": self.user.id,
            "opponent": self.opponent2.email,
        }

        self.auth_client.login(username=self.user.email, password="admin")
        self.auth_client.post(reverse("create_battle"), battle_data)
        self.auth_client.post(reverse("create_battle"), battle2_data)

        battle = Battle.objects.filter(creator=self.user)
        assert len(battle) == 2

        battle1 = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        assert len(battle1) == 1

        battle1 = Battle.objects.get(creator=self.user, opponent=self.opponent)
        self.assertCountEqual(battle1.creator.email, self.user.email)
        self.assertCountEqual(battle1.opponent.email, self.opponent.email)

        battle2 = Battle.objects.filter(creator=self.user, opponent=self.opponent2)
        assert len(battle2) == 1

        battle2 = Battle.objects.get(creator=self.user, opponent=self.opponent2)
        self.assertCountEqual(battle2.creator.email, self.user.email)
        self.assertCountEqual(battle2.opponent.email, self.opponent2.email)
