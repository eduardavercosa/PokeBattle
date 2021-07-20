from django.test import TestCase

from pokemon.helpers import get_pokemon_from_api, is_team_valid


class PokemonSumTest(TestCase):
    def test_sum_success(self):
        pokemon = [
            get_pokemon_from_api("pidgeot"),
            get_pokemon_from_api("pidgey"),
            get_pokemon_from_api("pidgeotto"),
        ]
        sum_pokemon = is_team_valid(pokemon)
        self.assertTrue(sum_pokemon)

    def test_sum_fail(self):
        pokemon = [
            get_pokemon_from_api("pidgeot"),
            get_pokemon_from_api("beedrill"),
            get_pokemon_from_api("pidgeotto"),
        ]
        sum_pokemon = is_team_valid(pokemon)
        self.assertFalse(sum_pokemon)
