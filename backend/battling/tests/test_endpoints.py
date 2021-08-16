from unittest.mock import patch

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battling.api.serializers import BattleSerializer
from battling.models import Battle, PokemonTeam, Team
from battling.tasks import run_battle_and_send_result_email
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


class BattleDetailEndpointTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.user2 = baker.make("users.User")

    def test_user_cannot_acess_battle_detail_logged_out(self):
        self.auth_client.logout()
        response = self.client.get(reverse("battle-list"))
        self.assertEqual(response.status_code, 403)

    def test_battle_not_found(self):
        response = self.auth_client.get(reverse("battle-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 404)

    def test_battle_detail_exists(self):
        battle = baker.make("battling.Battle", creator=self.user, opponent=self.user2)
        response = self.auth_client.get(reverse("battle-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, 200)

        expected_response = BattleSerializer([battle], many=True)
        self.assertCountEqual(expected_response.data, [response.json()])

        
class CreateTeamEndpointTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battling.Battle", creator=self.user, opponent=self.opponent)
        self.creator_team = baker.make("battling.Team", battle=self.battle, trainer=self.user)
        self.opponent_team = baker.make("battling.Team", battle=self.battle, trainer=self.opponent)

        self.pokemon_1 = baker.make(
            "pokemon.Pokemon", name="pikachu", poke_id=15, attack=10, defense=10, hp=10
        )
        self.pokemon_2 = baker.make(
            "pokemon.Pokemon", name="bulbasaur", poke_id=16, attack=10, defense=10, hp=10
        )
        self.pokemon_3 = baker.make(
            "pokemon.Pokemon", name="squirtle", poke_id=17, attack=10, defense=10, hp=10
        )

    def test_create_team(self):
        pokemons = [self.pokemon_1.id, self.pokemon_2.id, self.pokemon_3.id]
        pokemon_data = {"pokemons_ids": pokemons}

        self.auth_client.put(
            reverse("create-team", kwargs={"pk": self.creator_team.id}),
            pokemon_data,
            follow=True,
            content_type="application/json",
        )

        pokemon_team = PokemonTeam.objects.filter(team=self.creator_team.id)
        pokemon_ids = [pk.pokemon.id for pk in pokemon_team]

        self.assertEqual(pokemon_data["pokemons_ids"], pokemon_ids)

    def test_does_not_create_team_with_user_not_logged(self):
        self.auth_client.logout()
        pokemons = [self.pokemon_1.id, self.pokemon_2.id, self.pokemon_3.id]
        pokemon_data = {"pokemons_ids": pokemons}

        response = self.auth_client.put(
            reverse("create-team", kwargs={"pk": self.creator_team.id}),
            pokemon_data,
            follow=True,
            content_type="application/json",
        )

        pokemon_team = PokemonTeam.objects.filter(team=self.creator_team.id)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(pokemon_team)

    def test_does_not_create_team_with_repeated_pokemon(self):
        pokemons = [self.pokemon_1.id, self.pokemon_1.id, self.pokemon_3.id]
        pokemon_data = {"pokemons_ids": pokemons}

        response = self.auth_client.put(
            reverse("create-team", kwargs={"pk": self.creator_team.id}),
            pokemon_data,
            follow=True,
            content_type="application/json",
        )

        self.assertEqual(
            response.json()["non_field_errors"][0],
            "You can't choose the same Pokemon more than once.",
        )

    @patch("services.email.send_templated_mail")
    def test_run_battle_and_send_result_email(self, email_mock):

        pokemon_list = [self.pokemon_1, self.pokemon_2, self.pokemon_3]

        for count, pokemon in enumerate(pokemon_list):
            PokemonTeam.objects.create(team=self.creator_team, pokemon=pokemon, order=count + 1)

        for count, pokemon in enumerate(pokemon_list):
            PokemonTeam.objects.create(team=self.opponent_team, pokemon=pokemon, order=count + 1)

        run_battle_and_send_result_email(self.battle.id)

        self.assertEqual(
            self.opponent, Battle.objects.get(creator=self.user, opponent=self.opponent).winner
        )
        battle = Battle.objects.get(creator=self.user, opponent=self.opponent)

        email_mock.assert_called_with(
            template_name="battle_result",
            from_email=settings.FROM_EMAIL,
            recipient_list=[battle.creator.email, battle.opponent.email],
            context={
                "battle_creator": battle.creator.email.split("@")[0],
                "battle_opponent": battle.opponent.email.split("@")[0],
                "battle_winner": battle.winner.email.split("@")[0],
                "battle_id": battle.id,
                "battle_details_url": settings.HOST + reverse("battle_detail", args=[battle.id]),
            },
        )
