from django.test import Client, TestCase
from django.urls import reverse

from model_bakery import baker

from battling.models import Battle


class CreateBattleViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.creator = baker.make("users.User")
        self.creator.set_password("admin")
        self.creator.save()
        self.opponent = baker.make("users.User")
        self.opponent2 = baker.make("users.User")

    def test_create_battle_with_user_not_logged(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.opponent.email,
        }

        self.client.post(reverse("create_battle"), battle_data)
        battle = Battle.objects.filter(creator=self.creator, opponent=self.opponent)

        self.assertFalse(battle)

    def test_create_one_battle(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.opponent.email,
        }

        self.client.login(username=self.creator.email, password="admin")
        self.client.post(reverse("create_battle"), battle_data)
        battle = Battle.objects.get(creator=self.creator, opponent=self.opponent)

        self.assertCountEqual(battle.creator.email, self.creator.email)
        self.assertCountEqual(battle.opponent.email, self.opponent.email)

    def test_create_battle_with_multiple_requests(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.opponent.email,
        }

        battle2_data = {
            "creator": self.creator.id,
            "opponent": self.opponent2.email,
        }

        self.client.login(username=self.creator.email, password="admin")
        self.client.post(reverse("create_battle"), battle_data)
        self.client.post(reverse("create_battle"), battle2_data)

        battle = Battle.objects.filter(creator=self.creator)
        assert len(battle) == 2

        battle1 = Battle.objects.get(creator=self.creator, opponent=self.opponent)
        assert len(battle1) == 1
        self.assertCountEqual(battle.creator.email, self.creator.email)
        self.assertCountEqual(battle.opponent.email, self.opponent.email)

        battle2 = Battle.objects.get(creator=self.creator, opponent=self.opponent2)
        assert len(battle2) == 1
        self.assertCountEqual(battle.creator.email, self.creator.email)
        self.assertCountEqual(battle.opponent.email, self.opponent2.email)
