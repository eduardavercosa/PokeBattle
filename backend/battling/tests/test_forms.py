from unittest.mock import patch

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
        form = CreateTeamForm(
            data={
                "pokemon_1": "pikachu",
                "pokemon_1_position": "1",
                "pokemon_2": "pidgey",
                "pokemon_2_position": "2",
                "pokemon_3": "beedrill",
                "pokemon_3_position": "3",
            }
        )

        self.assertTrue(form.is_valid())

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

    @patch("pokemon.helpers.get_pokemon_from_api")
    def test_create_team_form_calls_get_pokemon_from_api(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "pikachu":
                fake_json = {
                    "defense": 40,
                    "attack": 55,
                    "hp": 35,
                    "name": "pikachu",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 25,
                }
            elif pokemon_name == "pidgey":
                fake_json = {
                    "defense": 50,
                    "attack": 25,
                    "hp": 15,
                    "name": "pidgey",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 15,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_data = {
            "pokemon_1": "pikachu",
            "pokemon_1_position": 1,
            "pokemon_2": "pidgey",
            "pokemon_2_position": 2,
            "pokemon_3": "bulbasaur",
            "pokemon_3_position": 3,
        }

        form = CreateTeamForm(data=pokemon_data)
        form.instance = self.team

        if form.is_valid():
            response = form.save()
            pokemon_team = PokemonTeam.objects.filter(team=response)

        self.assertEqual(pokemon_team[0].pokemon.name, pokemon_data["pokemon_1"])
        self.assertEqual(pokemon_team[1].pokemon.name, pokemon_data["pokemon_2"])
        self.assertEqual(pokemon_team[2].pokemon.name, pokemon_data["pokemon_3"])
