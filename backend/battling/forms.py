from django import forms

from battling.models import Battle, PokemonTeam, Team
from pokemon.helpers import (
    get_or_create_pokemon,
    get_pokemon_from_api,
    has_repeated_positions,
    is_team_valid,
    pokemon_in_api,
)
from users.models import User


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])


POSITION_CHOICES = [(1, 1), (2, 2), (3, 3)]


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "pokemon_1",
            "pokemon_1_position",
            "pokemon_2",
            "pokemon_2_position",
            "pokemon_3",
            "pokemon_3_position",
        ]

    pokemon_1_position = forms.TypedChoiceField(
        choices=POSITION_CHOICES, coerce=int, label="Pokemon position"
    )
    pokemon_2_position = forms.TypedChoiceField(
        choices=POSITION_CHOICES, coerce=int, label="Pokemon position"
    )
    pokemon_3_position = forms.TypedChoiceField(
        choices=POSITION_CHOICES, coerce=int, label="Pokemon position"
    )

    pokemon_1 = forms.CharField(
        label="Pokemon 1",
        required=True,
    )
    pokemon_2 = forms.CharField(
        label="Pokemon 2",
        required=True,
    )
    pokemon_3 = forms.CharField(
        label="Pokemon 3",
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        pokemon_names = [
            cleaned_data["pokemon_1"],
            cleaned_data["pokemon_2"],
            cleaned_data["pokemon_3"],
        ]
        for pokemon in pokemon_names:
            pokemon_exists_in_api = pokemon_in_api(pokemon)
            if not pokemon_exists_in_api:
                raise forms.ValidationError("ERROR: Choose only existing Pokemon.")

        pokemon_position_list = [
            (cleaned_data["pokemon_1_position"]),
            (cleaned_data["pokemon_2_position"]),
            (cleaned_data["pokemon_3_position"]),
        ]
        is_any_position_repeated = has_repeated_positions(pokemon_position_list)

        if is_any_position_repeated:
            raise forms.ValidationError("Each Pokemon must have a unique position.")

        pokemon_data = [
            get_pokemon_from_api(str(cleaned_data["pokemon_1"])),
            get_pokemon_from_api(str(cleaned_data["pokemon_2"])),
            get_pokemon_from_api(str(cleaned_data["pokemon_3"])),
        ]
        is_pokemon_sum_valid = is_team_valid(pokemon_data)

        if not is_pokemon_sum_valid:
            raise forms.ValidationError("ERROR: Your pokemons sum more than 600 points.")

        pokemons = get_or_create_pokemon(pokemon_data)
        cleaned_data["pokemon_1"] = pokemons[0]
        cleaned_data["pokemon_2"] = pokemons[1]
        cleaned_data["pokemon_3"] = pokemons[2]

        return cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        self.instance.pokemons.clear()

        PokemonTeam.objects.create(
            team=self.instance, pokemon=data["pokemon_1"], order=data["pokemon_1_position"]
        )
        PokemonTeam.objects.create(
            team=self.instance, pokemon=data["pokemon_2"], order=data["pokemon_2_position"]
        )
        PokemonTeam.objects.create(
            team=self.instance, pokemon=data["pokemon_3"], order=data["pokemon_3_position"]
        )

        return self.instance
