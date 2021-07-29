from unittest.mock import patch

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battling.models import Battle, PokemonTeam, Team
from battling.tasks import run_battle_and_send_result_email
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

        self.auth_client.post(reverse("create_battle"), battle_data)
        battle = Battle.objects.get(creator=self.user, opponent=self.opponent)

        self.assertEqual(battle.creator.email, self.user.email)
        self.assertEqual(battle.opponent.email, self.opponent.email)

    def test_create_battle_with_multiple_requests(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        battle2_data = {
            "creator": self.user.id,
            "opponent": self.opponent2.email,
        }

        self.auth_client.post(reverse("create_battle"), battle_data)
        self.auth_client.post(reverse("create_battle"), battle2_data)

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
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        self.auth_client.post(reverse("create_battle"), battle_data)

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


class CreateTeamViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battling.Battle", creator=self.user, opponent=self.opponent)
        self.creator_team = baker.make("battling.Team", battle=self.battle, trainer=self.user)
        self.opponent_team = baker.make("battling.Team", battle=self.battle, trainer=self.opponent)

        self.pokemon_list = [
            baker.make("pokemon.Pokemon", name="pidgey", attack=10, defense=10, hp=10),
            baker.make("pokemon.Pokemon", name="pidgeotto", attack=10, defense=10, hp=10),
            baker.make("pokemon.Pokemon", name="pidgeot", attack=10, defense=10, hp=10),
        ]

    def test_create_team(self):
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.opponent_team.id}), pokemon_data, follow=True
        )

        pokemon_team = PokemonTeam.objects.filter(team=self.opponent_team.id)

        pokemon_set = {
            pokemon_data["pokemon_1"],
            pokemon_data["pokemon_2"],
            pokemon_data["pokemon_3"],
        }

        self.assertEqual(pokemon_set, {pk.pokemon.name for pk in pokemon_team})

    def test_does_not_create_team_with_user_not_logged(self):
        self.auth_client.logout()
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.opponent_team.id}), pokemon_data, follow=True
        )

        team_id = str(self.opponent_team.id)
        self.assertRedirects(response, "/account/login/?next=/team/" + team_id + "/edit/")

    def test_does_not_create_team_with_wrong_pokemon_name(self):
        pokemon_data = {
            "pokemon_1": "random",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.opponent_team.id}), pokemon_data, follow=True
        )

        self.assertEqual(
            response.context_data["form"].errors["__all__"][0],
            "ERROR: Choose only existing Pokemon.",
        )

    def test_does_not_create_team_with_same_pokemon_position(self):
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 1,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.opponent_team.id}), pokemon_data, follow=True
        )

        self.assertEqual(
            response.context_data["form"].errors["__all__"][0],
            "Each Pokemon must have a unique position.",
        )

    def test_does_not_create_team_with_repeated_pokemon(self):
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeotto",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.opponent_team.id}), pokemon_data, follow=True
        )

        self.assertEqual(
            response.context_data["form"].errors["__all__"][0],
            "You can't choose the same Pokemon more than once.",
        )

    def test_run_battle_and_send_result_email(self):

        for count, pokemon in enumerate(self.pokemon_list):
            PokemonTeam.objects.create(team=self.creator_team, pokemon=pokemon, order=count + 1)

        for count, pokemon in enumerate(self.pokemon_list):
            PokemonTeam.objects.create(team=self.opponent_team, pokemon=pokemon, order=count + 1)

        run_battle_and_send_result_email(self.battle.id)

        self.assertEqual(
            self.opponent, Battle.objects.get(creator=self.user, opponent=self.opponent).winner
        )
