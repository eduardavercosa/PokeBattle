from django.test import Client, TestCase

from model_bakery import baker

from battling.models import PokemonTeam
from pokemon.models import Pokemon


class CreateBattleTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.creator = baker.make("users.User")
        self.creator.set_password("admin")
        self.creator.save()
        self.opponent = baker.make("users.User")

    def test_create_battle(self):
        self.client.login(username=self.creator.email, password="admin")
        battle = baker.make(
            "battling.Battle", creator=self.creator, opponent=self.opponent, _quantity=2
        )
        battle_data = {
            "creator": self.creator,
            "opponent": self.opponent,
        }

        response = self.client.get("/battle/list/", battle_data)
        response_qs = response.context_data.get("battle_list")
        self.assertCountEqual(battle, response_qs)


class CreatePokemonTest(TestCase):
    def setUp(self):
        self.creator = baker.make("users.User")
        self.creator.set_password("admin")
        self.creator.save()

        self.battle = baker.make("battling.Battle", creator=self.creator, _quantity=1)
        self.team = baker.make(
            "battling.Team", battle=self.battle[0], trainer=self.creator, _quantity=1
        )

        self.pokemon_1 = baker.make(
            "pokemon.Pokemon",
            poke_id=18,
            attack=70,
            defense=70,
            hp=101,
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

        self.pokemon_1.save()
        self.pokemon_2.save()
        self.pokemon_3.save()

    def test_create_pokemon(self):
        pokemon_1, pokemon_2, pokemon_3 = (
            Pokemon.objects.get(poke_id=18),
            Pokemon.objects.get(poke_id=16),
            Pokemon.objects.get(poke_id=17),
        )

        baker.make("battling.PokemonTeam", team=self.team[0], pokemon=pokemon_1)
        baker.make("battling.PokemonTeam", team=self.team[0], pokemon=pokemon_2)
        baker.make("battling.PokemonTeam", team=self.team[0], pokemon=pokemon_3)

        self.assertTrue(
            PokemonTeam.objects.filter(team=self.team[0], pokemon=pokemon_1).exists(),
        )
        self.assertTrue(
            PokemonTeam.objects.filter(team=self.team[0], pokemon=pokemon_2).exists(),
        )
        self.assertTrue(
            PokemonTeam.objects.filter(team=self.team[0], pokemon=pokemon_3).exists(),
        )
