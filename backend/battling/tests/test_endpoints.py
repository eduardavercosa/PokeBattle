from unittest.mock import patch

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battling.models import Battle, PokemonTeam
from battling.tasks import run_battle_and_send_result_email
from common.utils.tests import TestCaseUtils


class CreateTeamEndpointTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battling.Battle", creator=self.user, opponent=self.opponent)
        self.creator_team = baker.make("battling.Team", battle=self.battle, trainer=self.user)
        self.opponent_team = baker.make("battling.Team", battle=self.battle, trainer=self.opponent)

        self.pokemon_1 = baker.make(
            "pokemon.Pokemon", name="pikachu", poke_id=15, attack=10, defense=10, hp=10
        )
        self.pokemon_2 = baker.make(
            "pokemon.Pokemon", name="bulbasaur", poke_id=16, attack=10, defense=10, hp=10
        )
        self.pokemon_3 = baker.make(
            "pokemon.Pokemon", name="squirtle", poke_id=17, attack=10, defense=10, hp=10
        )

    def test_create_team(self):
        pokemons = [self.pokemon_1.id, self.pokemon_2.id, self.pokemon_3.id]
        pokemon_data = {"pokemons_ids": pokemons}

        self.auth_client.put(
            reverse("create-team", kwargs={"pk": self.creator_team.id}),
            pokemon_data,
            follow=True,
            content_type="application/json",
        )

        pokemon_team = PokemonTeam.objects.filter(team=self.creator_team.id)

        pokemon_set = {pk for pk in pokemon_data["pokemons_ids"]}

        self.assertEqual(pokemon_set, {pk.pokemon.id for pk in pokemon_team})

    def test_does_not_create_team_with_user_not_logged(self):
        self.auth_client.logout()
        pokemons = [self.pokemon_1.id, self.pokemon_2.id, self.pokemon_3.id]
        pokemon_data = {"pokemons_ids": pokemons}

        response = self.auth_client.put(
            reverse("create-team", kwargs={"pk": self.creator_team.id}),
            pokemon_data,
            follow=True,
            content_type="application/json",
        )

        pokemon_team = PokemonTeam.objects.filter(team=self.creator_team.id)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(pokemon_team)

    def test_does_not_create_team_with_repeated_pokemon(self):
        pokemons = [self.pokemon_1.id, self.pokemon_1.id, self.pokemon_3.id]
        pokemon_data = {"pokemons_ids": pokemons}

        response = self.auth_client.put(
            reverse("create-team", kwargs={"pk": self.creator_team.id}),
            pokemon_data,
            follow=True,
            content_type="application/json",
        )

        self.assertEqual(
            response.json()["non_field_errors"][0],
            "You can't choose the same Pokemon more than once.",
        )

    @patch("services.email.send_templated_mail")
    def test_run_battle_and_send_result_email(self, email_mock):

        pokemon_list = [self.pokemon_1, self.pokemon_2, self.pokemon_3]

        for count, pokemon in enumerate(pokemon_list):
            PokemonTeam.objects.create(team=self.creator_team, pokemon=pokemon, order=count + 1)

        for count, pokemon in enumerate(pokemon_list):
            PokemonTeam.objects.create(team=self.opponent_team, pokemon=pokemon, order=count + 1)

        run_battle_and_send_result_email(self.battle.id)

        self.assertEqual(
            self.opponent, Battle.objects.get(creator=self.user, opponent=self.opponent).winner
        )
        battle = Battle.objects.get(creator=self.user, opponent=self.opponent)

        email_mock.assert_called_with(
            template_name="battle_result",
            from_email=settings.FROM_EMAIL,
            recipient_list=[battle.creator.email, battle.opponent.email],
            context={
                "battle_creator": battle.creator.email.split("@")[0],
                "battle_opponent": battle.opponent.email.split("@")[0],
                "battle_winner": battle.winner.email.split("@")[0],
                "battle_id": battle.id,
                "battle_details_url": settings.HOST + reverse("battle_detail", args=[battle.id]),
            },
        )
