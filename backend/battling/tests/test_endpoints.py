from unittest.mock import patch

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battling.api.serializers import BattleSerializer
from battling.models import Battle, Team
from common.utils.tests import TestCaseUtils


class CreateBattleEndpointTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.opponent2 = baker.make("users.User")

    def test_cannot_create_battle_with_user_not_logged(self):
        self.auth_client.logout()
        battle_data = {
            "creator_id": self.user.id,
            "opponent_id": self.opponent.id,
        }

        response = self.auth_client.post(reverse("create-battle"), battle_data)
        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(battle)

    def test_user_cannot_challenge_itself(self):
        battle_data = {
            "creator_id": self.user.id,
            "opponent_id": self.user.id,
        }
        response = self.auth_client.post(reverse("create-battle"), battle_data)

        self.assertEqual(
            response.json()["non_field_errors"][0],
            "ERROR: You can't challenge yourself.",
        )

    def test_create_battle_successfully(self):
        battle_data = {
            "creator_id": self.user.id,
            "opponent_id": self.opponent.id,
        }

        response = self.auth_client.post(reverse("create-battle"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(battle)
        self.assertEqual(battle[0].creator.email, self.user.email)
        self.assertEqual(battle[0].opponent.email, self.opponent.email)

    def test_create_battle_with_multiple_requests(self):
        battle_data = {
            "creator_id": self.user.id,
            "opponent_id": self.opponent.id,
        }

        battle2_data = {
            "creator_id": self.user.id,
            "opponent_id": self.opponent2.id,
        }

        response = self.auth_client.post(reverse("create-battle"), battle_data)
        self.assertEqual(response.status_code, 201)

        response = self.auth_client.post(reverse("create-battle"), battle2_data)
        self.assertEqual(response.status_code, 201)

        battle = Battle.objects.filter(creator=self.user)
        assert len(battle) == 2

        battle1 = Battle.objects.get(creator=self.user, opponent=self.opponent)
        self.assertEqual(battle1.creator.email, self.user.email)
        self.assertEqual(battle1.opponent.email, self.opponent.email)

        battle2 = Battle.objects.get(creator=self.user, opponent=self.opponent2)
        self.assertEqual(battle2.creator.email, self.user.email)
        self.assertEqual(battle2.opponent.email, self.opponent2.email)

    @patch("services.email.send_templated_mail")
    def test_if_invitation_email_is_sent(self, mock_templated_mail):
        battle_data = {
            "creator_id": self.user.id,
            "opponent_id": self.opponent.id,
        }

        self.auth_client.post(reverse("create-battle"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)

        self.assertTrue(battle)

        opponent_team = Team.objects.filter(trainer=self.opponent)[0]

        mock_templated_mail.assert_called_with(
            template_name="battle_invite",
            from_email=settings.FROM_EMAIL,
            recipient_list=[self.opponent.email],
            context={
                "battle_creator": self.user.email.split("@")[0],
                "battle_opponent": self.opponent.email.split("@")[0],
                "battle_invite_url": settings.HOST
                + reverse("create_team", args=[opponent_team.id]),
                "battle_delete_url": settings.HOST + reverse("delete_battle", args=[battle[0].id]),
            },
        )


class BattleListEndpointTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.user2 = baker.make("users.User")

    def test_user_cannot_acess_battle_list_logged_out(self):
        self.auth_client.logout()
        response = self.client.get(reverse("battle-list"))
        self.assertEqual(response.status_code, 403)

    def test_no_battles_in_list(self):
        response = self.auth_client.get(reverse("battle-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_one_battle_in_list(self):
        battle = baker.make("battling.Battle", creator=self.user, opponent=self.user2)
        response = self.auth_client.get(reverse("battle-list"))

        self.assertEqual(response.status_code, 200)

        battles = Battle.objects.filter(creator=self.user, opponent=self.user2)
        assert len(battles) == 1

        expected_response = BattleSerializer([battle], many=True)
        self.assertCountEqual(expected_response.data, response.json())

    def test_a_few_battles_in_list(self):
        battle = baker.make("battling.Battle", creator=self.user, opponent=self.user2, _quantity=5)
        response = self.auth_client.get(reverse("battle-list"))

        self.assertEqual(response.status_code, 200)

        battles = Battle.objects.filter(creator=self.user, opponent=self.user2)
        assert len(battles) == 5

        expected_response = BattleSerializer(battle, many=True)
        self.assertCountEqual(expected_response.data, response.json())

    def test_a_lot_battle_in_list(self):
        battle = baker.make("battling.Battle", creator=self.user, opponent=self.user2, _quantity=50)
        response = self.auth_client.get(reverse("battle-list"))

        self.assertEqual(response.status_code, 200)

        battles = Battle.objects.filter(creator=self.user, opponent=self.user2)
        assert len(battles) == 50

        expected_response = BattleSerializer(battle, many=True)
        self.assertCountEqual(expected_response.data, response.json())

    def test_battle_with_multiple_requests_in_list(self):
        battle = baker.make("battling.Battle", creator=self.user, opponent=self.user2, _quantity=10)
        battle2 = baker.make("battling.Battle", creator=self.user2, opponent=self.user, _quantity=9)
        response = self.auth_client.get(reverse("battle-list"))

        self.assertEqual(response.status_code, 200)

        battles = Battle.objects.filter(creator=self.user, opponent=self.user2)
        battles2 = Battle.objects.filter(creator=self.user2, opponent=self.user)

        assert len(battles) == 10
        assert len(battles2) == 9

        all_battles = battle + battle2

        expected_response = BattleSerializer(all_battles, many=True)
        self.assertCountEqual(expected_response.data, response.json())
