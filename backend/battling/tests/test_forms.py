from battling.forms import CreateTeamForm
from common.utils.tests import TestCaseUtils


class CreateTeamFormTest(TestCaseUtils):
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
