from django import forms

from battling.models import Battle, PokemonTeam, Team
from pokemon.helpers import valid_team
from pokemon.models import Pokemon


class PokemonForm(forms.ModelForm):
    pokemon_1 = forms.ModelChoiceField(
        label="Pokemon 1",
        queryset=Pokemon.objects.all(),
        widget=forms.TextInput,
        required=True,
    )
    pokemon_2 = forms.ModelChoiceField(
        label="Pokemon 2",
        queryset=Pokemon.objects.all(),
        widget=forms.TextInput,
        required=True,
    )
    pokemon_3 = forms.ModelChoiceField(
        label="Pokemon 3",
        queryset=Pokemon.objects.all(),
        widget=forms.TextInput,
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        is_pokemon_sum_valid = valid_team(
            [
                self.cleaned_data["pokemon_1"],
                self.cleaned_data["pokemon_2"],
                self.cleaned_data["pokemon_3"],
            ]
        )

        if not is_pokemon_sum_valid:
            raise forms.ValidationError("ERROR: Your pokemons sum more than 600 points.")

        for i in range(1, 4):
            PokemonTeam.objects.create(
                team=Team.objects.last(), pokemon=cleaned_data["pokemon_" + str(i)], order=i
            )

        return cleaned_data


class PokemonForm2(forms.ModelForm):
    opponent_pokemon_1 = forms.ModelChoiceField(
        label="Pokemon 1",
        queryset=Pokemon.objects.all(),
        widget=forms.TextInput,
        required=True,
    )
    opponent_pokemon_2 = forms.ModelChoiceField(
        label="Pokemon 2",
        queryset=Pokemon.objects.all(),
        widget=forms.TextInput,
        required=True,
    )
    opponent_pokemon_3 = forms.ModelChoiceField(
        label="Pokemon 3",
        queryset=Pokemon.objects.all(),
        widget=forms.TextInput,
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        is_pokemon_sum_valid = valid_team(
            [
                self.cleaned_data["opponent_pokemon_1"],
                self.cleaned_data["opponent_pokemon_2"],
                self.cleaned_data["opponent_pokemon_3"],
            ]
        )

        if not is_pokemon_sum_valid:
            raise forms.ValidationError("ERROR: Your pokemons sum more than 600 points.")

        return cleaned_data


class CreatorForm(PokemonForm):
    class Meta:
        model = Battle
        fields = (
            "opponent",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
        )


class OpponentForm(PokemonForm2):
    class Meta:
        model = Battle
        fields = ["opponent_pokemon_1", "opponent_pokemon_2", "opponent_pokemon_3"]
