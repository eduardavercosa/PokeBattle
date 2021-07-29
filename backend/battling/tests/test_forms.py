from model_bakery import baker

from battling.forms import CreateTeamForm
from battling.models import PokemonTeam
from common.utils.tests import TestCaseUtils


class CreateTeamFormTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battling.Battle", creator=self.user, opponent=self.opponent)
        self.team = baker.make("battling.Team", battle=self.battle, trainer=self.user)

    def test_create_team_form_with_valid_data(self):
        pokemon_data = {
            "pokemon_1": "pikachu",
            "pokemon_1_position": "1",
            "pokemon_2": "pidgey",
            "pokemon_2_position": "2",
            "pokemon_3": "beedrill",
            "pokemon_3_position": "3",
        }

        form = CreateTeamForm(data=pokemon_data)
        self.assertTrue(form.is_valid())

        form.instance = self.team

        if form.is_valid():
            response = form.save()
            pokemon_team = PokemonTeam.objects.filter(team=response)

            self.assertEqual(
                (pokemon_team[0].pokemon.name, str(pokemon_team[0].order)),
                (pokemon_data["pokemon_1"], pokemon_data["pokemon_1_position"]),
            )
            self.assertEqual(
                (pokemon_team[1].pokemon.name, str(pokemon_team[1].order)),
                (pokemon_data["pokemon_2"], pokemon_data["pokemon_2_position"]),
            )
            self.assertEqual(
                (pokemon_team[2].pokemon.name, str(pokemon_team[2].order)),
                (pokemon_data["pokemon_3"], pokemon_data["pokemon_3_position"]),
            )

    def test_create_team_form_without_data(self):
        form = CreateTeamForm(data={})

        self.assertFalse(form.is_valid())

    def test_create_team_form_with_missing_pokemon(self):
        form = CreateTeamForm(
            data={
                "pokemon_1": "",
                "pokemon_1_position": "1",
                "pokemon_2": "pidgey",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertFalse(form.is_valid())

    def test_create_team_form_with_missing_position(self):
        form = CreateTeamForm(
            data={
                "pokemon_1": "pikachu",
                "pokemon_1_position": "",
                "pokemon_2": "pidgey",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertFalse(form.is_valid())

    def test_create_team_form_with_repeated_position(self):
        form = CreateTeamForm(
            data={
                "pokemon_1": "pikachu",
                "pokemon_1_position": "2",
                "pokemon_2": "pidgey",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertFalse(form.is_valid())

    def test_create_team_form_with_repeated_pokemon(self):
        form = CreateTeamForm(
            data={
                "pokemon_1": "pikachu",
                "pokemon_1_position": "1",
                "pokemon_2": "pikachu",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertFalse(form.is_valid())

    def test_create_team_form_with_more_than_600_points(self):
        form = CreateTeamForm(
            data={
                "pokemon_1": "pidgeotto",
                "pokemon_1_position": "1",
                "pokemon_2": "pidgeot",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertFalse(form.is_valid())

    def test_create_team_form_with_invalid_pokemon(self):
        form = CreateTeamForm(
            data={
                "pokemon_1": "invalid",
                "pokemon_1_position": "1",
                "pokemon_2": "pidgey",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertFalse(form.is_valid())
