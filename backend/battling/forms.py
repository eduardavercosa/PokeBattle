from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string

from battling.models import Battle, PokemonTeam, Team
from pokemon.helpers import (
    get_or_create_pokemon,
    get_pokemon_from_api,
    has_repeated_positions,
    is_team_valid,
    pokemon_in_api,
)
from services.email import send_battle_invite
from users.helper import is_email_valid
from users.models import User


is_guest = False


class CreateBattleForm(forms.ModelForm):
    opponent = forms.EmailField(
        required=True,
    )

    class Meta:
        model = Battle
        fields = [
            "creator",
            "opponent",
        ]

    def __init__(self, *args, **kwargs):
        super(CreateBattleForm, self).__init__(*args, **kwargs)
        self.fields["creator"].widget = forms.HiddenInput()

    def clean_opponent(self):
        opponent_email = self.cleaned_data["opponent"]
        try:
            opponent = User.objects.get(email=opponent_email)
        except User.DoesNotExist:
            global is_guest
            is_guest = True
            opponent = User.objects.create(email=opponent_email)
            random_password = get_random_string(length=64)
            opponent.set_password(random_password)
            opponent.save()
        return opponent

    def clean(self):
        cleaned_data = super().clean()

        try:
            opponent = str(cleaned_data["opponent"])
        except Exception:
            raise forms.ValidationError("ERROR: Please, type a valid email.")

        if not is_email_valid(opponent):
            raise forms.ValidationError("ERROR: Please, type a valid email.")

        if cleaned_data["opponent"] == cleaned_data["creator"]:
            raise forms.ValidationError("ERROR: You can't challenge yourself.")

    def save(self):
        instance = super().save()
        battle = self.instance
        global is_guest

        opponent_team_id = Team.objects.create(battle=battle, trainer=battle.opponent)

        if is_guest is False:
            send_battle_invite(battle, opponent_team_id.id)

        else:
            invite_form = PasswordResetForm(data={"email": battle.opponent.email})
            invite_form.is_valid()
            invite_form.save(
                self,
                subject_template_name="registration/password_reset_subject.txt",
                email_template_name="registration/password_reset_email.html",
                use_https=False,
                token_generator=default_token_generator,
                from_email="eduardavercosa@vinta.com.br",
                request=None,
                html_email_template_name=None,
            )
        return instance


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
