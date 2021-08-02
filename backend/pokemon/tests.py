from model_bakery import baker

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
