from django.test import TestCase

from model_bakery import baker

from pokemon.helpers import is_team_valid
from pokemon.models import Pokemon


class PokemonSumTest(TestCase):
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

        self.pokemon_1.save()
        self.pokemon_2.save()
        self.pokemon_3.save()
        self.pokemon_4.save()

    def test_team_sum(self):
        pokemon_1 = {
            "poke_id": Pokemon.objects.get(poke_id=15).poke_id,
            "defense": Pokemon.objects.get(poke_id=15).defense,
            "attack": Pokemon.objects.get(poke_id=15).attack,
            "hp": Pokemon.objects.get(poke_id=15).hp,
        }
        pokemon_2 = {
            "poke_id": Pokemon.objects.get(poke_id=16).poke_id,
            "defense": Pokemon.objects.get(poke_id=16).defense,
            "attack": Pokemon.objects.get(poke_id=16).attack,
            "hp": Pokemon.objects.get(poke_id=16).hp,
        }
        pokemon_3 = {
            "poke_id": Pokemon.objects.get(poke_id=17).poke_id,
            "defense": Pokemon.objects.get(poke_id=17).defense,
            "attack": Pokemon.objects.get(poke_id=17).attack,
            "hp": Pokemon.objects.get(poke_id=17).hp,
        }
        pokemon_4 = {
            "poke_id": Pokemon.objects.get(poke_id=18).poke_id,
            "defense": Pokemon.objects.get(poke_id=18).defense,
            "attack": Pokemon.objects.get(poke_id=18).attack,
            "hp": Pokemon.objects.get(poke_id=18).hp,
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
