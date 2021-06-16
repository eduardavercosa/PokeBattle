from django import forms

from battling.models import Battle, PokemonTeam, Team
from pokemon.helpers import save_pokemon, valid_team
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
    )
    pokemon_2 = forms.IntegerField(
        label="Pokemon 2",
        required=True,
    )
    pokemon_3 = forms.IntegerField(
        label="Pokemon 3",
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        cleaned_data["pokemon_1"] = save_pokemon(str(cleaned_data["pokemon_1"]))
        cleaned_data["pokemon_2"] = save_pokemon(str(cleaned_data["pokemon_2"]))
        cleaned_data["pokemon_3"] = save_pokemon(str(cleaned_data["pokemon_3"]))

        is_pokemon_sum_valid = valid_team(
            [
                self.cleaned_data["pokemon_1"],
                self.cleaned_data["pokemon_2"],
                self.cleaned_data["pokemon_3"],
            ]
        )

        if not is_pokemon_sum_valid:
            raise forms.ValidationError("ERROR: Your pokemons sum more than 600 points.")

        return cleaned_data

    def save(self, commit=True):
        data = self.clean()
        self.instance.pokemons.clear()

        PokemonTeam.objects.create(team=self.instance, pokemon=data["pokemon_1"], order=1)
        PokemonTeam.objects.create(team=self.instance, pokemon=data["pokemon_2"], order=2)
        PokemonTeam.objects.create(team=self.instance, pokemon=data["pokemon_3"], order=3)

        return self.instance
