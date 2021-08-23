from model_bakery import baker

from common.utils.tests import TestCaseUtils
from pokemon.helpers import has_repeated_pokemon, is_team_valid


class PokemonHelpersTest(TestCaseUtils):
    def test_has_repeated_pokemon(self):
        pokemon_1 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )
        pokemon_2 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )

        pokemons_list = [pokemon_1, pokemon_1, pokemon_2]

        self.assertTrue(has_repeated_pokemon(pokemons_list))

    def test_does_not_have_repeated_pokemon(self):
        pokemon_1 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )
        pokemon_2 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )
        pokemon_3 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )

        pokemons_list = [pokemon_1, pokemon_3, pokemon_2]

        self.assertFalse(has_repeated_pokemon(pokemons_list))

    def test_team_is_valid(self):
        pokemon_1 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )
        pokemon_2 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )
        pokemon_3 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=45,
            hp=75,
        )

        pokemons_list = [pokemon_1, pokemon_3, pokemon_2]

        self.assertTrue(is_team_valid(pokemons_list))

    def test_team_is_not_valid(self):
        pokemon_1 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=80,
            defense=100,
            hp=100,
        )
        pokemon_2 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=100,
            defense=100,
            hp=75,
        )
        pokemon_3 = baker.make(
            "pokemon.Pokemon",
            poke_id=15,
            attack=100,
            defense=45,
            hp=100,
        )

        pokemons_list = [pokemon_1, pokemon_3, pokemon_2]

        self.assertFalse(is_team_valid(pokemons_list))
