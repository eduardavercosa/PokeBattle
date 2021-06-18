from django import forms

from battling.models import Battle, PokemonTeam, Team
from pokemon.helpers import get_or_create_pokemon, get_pokemon_from_api, is_team_valid
from users.models import User


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
        ]

    pokemon_1 = forms.IntegerField(
        label="Pokemon 1",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_2 = forms.IntegerField(
        label="Pokemon 2",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_3 = forms.IntegerField(
        label="Pokemon 3",
        required=True,
        min_value=1,
        max_value=898,
    )

    def clean(self):
        cleaned_data = super().clean()

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

        PokemonTeam.objects.create(team=self.instance, pokemon=data["pokemon_1"], order=1)
        PokemonTeam.objects.create(team=self.instance, pokemon=data["pokemon_2"], order=2)
        PokemonTeam.objects.create(team=self.instance, pokemon=data["pokemon_3"], order=3)

        return self.instance
