from unittest.mock import patch

from model_bakery import baker

from battling.forms import CreateTeamForm
from battling.models import PokemonTeam
from common.utils.tests import TestCaseUtils
from pokemon.helpers import is_team_valid


class PokemonSumTest(TestCaseUtils):
    def setUp(self):
        self.pokemon_1 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )
        self.pokemon_2 = baker.make(
            "pokemon.Pokemon",
            poke_id=16,
            attack=35,
            defense=35,
            hp=56,
        )
        self.pokemon_3 = baker.make(
            "pokemon.Pokemon",
            poke_id=17,
            attack=50,
            defense=50,
            hp=71,
        )
        self.pokemon_4 = baker.make(
            "pokemon.Pokemon",
            poke_id=18,
            attack=70,
            defense=70,
            hp=101,
        )

    def test_if_team_is_valid(self):
        pokemon_1 = {
            "poke_id": self.pokemon_1.poke_id,
            "defense": self.pokemon_1.defense,
            "attack": self.pokemon_1.attack,
            "hp": self.pokemon_1.hp,
        }
        pokemon_2 = {
            "poke_id": self.pokemon_2.poke_id,
            "defense": self.pokemon_2.defense,
            "attack": self.pokemon_2.attack,
            "hp": self.pokemon_2.hp,
        }
        pokemon_3 = {
            "poke_id": self.pokemon_3.poke_id,
            "defense": self.pokemon_3.defense,
            "attack": self.pokemon_3.attack,
            "hp": self.pokemon_3.hp,
        }
        pokemon_4 = {
            "poke_id": self.pokemon_4.poke_id,
            "defense": self.pokemon_4.defense,
            "attack": self.pokemon_4.attack,
            "hp": self.pokemon_4.hp,
        }

        pokemon_team_1 = [
            pokemon_2,
            pokemon_3,
            pokemon_4,
        ]

        pokemon_team_2 = [
            pokemon_1,
            pokemon_3,
            pokemon_4,
        ]

        sum_pokemon_team_1 = is_team_valid(pokemon_team_1)
        sum_pokemon_team_2 = is_team_valid(pokemon_team_2)

        self.assertTrue(sum_pokemon_team_1)
        self.assertFalse(sum_pokemon_team_2)


class PokemonApiIntegrationTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battling.Battle", creator=self.user, opponent=self.opponent)
        self.team = baker.make("battling.Team", battle=self.battle, trainer=self.user)

    @patch("pokemon.helpers.get_pokemon_from_api")
    def test_if_pokemon_api_integration_returns_pokemon_data(self, mock_get_pokemon):
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
