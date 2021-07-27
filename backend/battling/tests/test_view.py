from django.urls import reverse

from model_bakery import baker

from battling.models import Battle, PokemonTeam
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


class CreateTeamViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battling.Battle", creator=self.user, opponent=self.opponent)
        self.team = baker.make("battling.Team", battle=self.battle, trainer=self.user)
        self.team = baker.make("battling.Team", battle=self.battle, trainer=self.opponent)

        baker.make("pokemon.Pokemon", name="pidgey", attack=10, defense=10, hp=10)
        baker.make("pokemon.Pokemon", name="pidgeotto", attack=10, defense=10, hp=10)
        baker.make("pokemon.Pokemon", name="pidgeot", attack=10, defense=10, hp=10)

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
            reverse("create_team", kwargs={"pk": self.team.id}), pokemon_data, follow=True
        )

        pokemon_team = PokemonTeam.objects.filter(team=self.team.id)

        pokemon_set = [
            pokemon_data["pokemon_1"],
            pokemon_data["pokemon_2"],
            pokemon_data["pokemon_3"],
        ]

        self.assertEqual(set(pokemon_set), set([pk.pokemon.name for pk in pokemon_team]))

    def test_create_team_with_user_not_logged(self):
        self.auth_client.logout()
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.team.id}), pokemon_data, follow=True
        )

        team = PokemonTeam.objects.filter(team=self.team.id)

        self.assertFalse(team)

    def test_create_team_with_wrong_pokemon_name(self):
        pokemon_data = {
            "pokemon_1": "random",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.team.id}), pokemon_data, follow=True
        )

        self.assertEqual(
            response.context_data["form"].errors["__all__"][0],
            "ERROR: Choose only existing Pokemon.",
        )

    def test_create_team_with_same_pokemon_position(self):
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeot",
            "pokemon_2_position": 1,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.team.id}), pokemon_data, follow=True
        )

        self.assertEqual(
            response.context_data["form"].errors["__all__"][0],
            "Each Pokemon must have a unique position.",
        )

    def test_create_team_with_repeated_pokemon(self):
        pokemon_data = {
            "pokemon_1": "pidgeotto",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgeotto",
            "pokemon_2_position": 2,
            "pokemon_3": "pidgey",
            "pokemon_3_position": 3,
        }
        response = self.auth_client.post(
            reverse("create_team", kwargs={"pk": self.team.id}), pokemon_data, follow=True
        )

        self.assertEqual(
            response.context_data["form"].errors["__all__"][0],
            "You can't choose the same Pokemon more than once.",
        )
