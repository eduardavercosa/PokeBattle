from rest_framework import serializers

from battling.models import Battle, PokemonTeam, Team
from battling.tasks import run_battle_and_send_result_email
from pokemon.helpers import (
    get_or_create_pokemon,
    get_pokemon_from_api,
    has_repeated_pokemon,
    has_repeated_positions,
    is_team_valid,
    pokemon_in_api,
)
from pokemon.models import Pokemon
from services.battles import set_up_battle_teams_and_send_invite_email
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id")


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ("id", "poke_id", "name", "img_url", "attack", "defense", "hp")


class TeamSerializer(serializers.ModelSerializer):
    trainer = UserSerializer()

    class Meta:
        model = Team
        fields = ("id", "battle", "trainer")


class PokemonTeamSerializer(serializers.ModelSerializer):
    teams = TeamSerializer()
    pokemon = PokemonSerializer(many=True)

    class Meta:
        model = PokemonTeam
        fields = ("id", "teams", "pokemon", "order")


class BattleSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    pokemon_teams = PokemonTeamSerializer(many=True, required=False)
    winner = UserSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(
        source="creator", queryset=User.objects.all(), required=False
    )
    opponent_id = serializers.PrimaryKeyRelatedField(
        source="opponent",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Battle
        fields = (
            "id",
            "creator",
            "creator_id",
            "opponent",
            "opponent_id",
            "teams",
            "pokemon_teams",
            "status",
            "winner",
        )

    def create(self, validated_data):
        validated_data["creator"] = self.context.get("request").user
        instance = super().create(validated_data)

        set_up_battle_teams_and_send_invite_email(instance)
        return instance


class BattleTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    pokemon_1 = serializers.CharField(style={"base_template": "textarea.html"}, required=False)
    pokemon_1_position = serializers.IntegerField(min_value=1, max_value=3, write_only=True)
    pokemon_2 = serializers.CharField(style={"base_template": "textarea.html"}, required=False)
    pokemon_2_position = serializers.IntegerField(min_value=1, max_value=3, write_only=True)
    pokemon_3 = serializers.CharField(style={"base_template": "textarea.html"}, required=False)
    pokemon_3_position = serializers.IntegerField(min_value=1, max_value=3, write_only=True)

    class Meta:
        model = PokemonTeam
        fields = (
            "id",
            "team",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "pokemon_1_position",
            "pokemon_2_position",
            "pokemon_3_position",
        )

    def validate(self, attrs):
        for field in [
            "pokemon_1",
            "pokemon_1_position",
            "pokemon_2",
            "pokemon_2_position",
            "pokemon_3",
            "pokemon_3_position",
        ]:
            if field not in attrs:
                raise serializers.ValidationError("ERROR: All fields are required.")

        pokemon_names = [
            attrs["pokemon_1"],
            attrs["pokemon_2"],
            attrs["pokemon_3"],
        ]
        for pokemon in pokemon_names:
            pokemon_exists_in_api = pokemon_in_api(pokemon)
            if not pokemon_exists_in_api:
                raise serializers.ValidationError("ERROR: Choose only existing Pokemon.")

        team_has_repeated_pokemon = has_repeated_pokemon(pokemon_names)
        if team_has_repeated_pokemon:
            raise serializers.ValidationError("You can't choose the same Pokemon more than once.")

        pokemon_position_list = [
            (attrs["pokemon_1_position"]),
            (attrs["pokemon_2_position"]),
            (attrs["pokemon_3_position"]),
        ]
        is_any_position_repeated = has_repeated_positions(pokemon_position_list)

        if is_any_position_repeated:
            raise serializers.ValidationError("Each Pokemon must have a unique position.")

        pokemon_data = [
            get_pokemon_from_api(str(attrs["pokemon_1"])),
            get_pokemon_from_api(str(attrs["pokemon_2"])),
            get_pokemon_from_api(str(attrs["pokemon_3"])),
        ]
        is_pokemon_sum_valid = is_team_valid(pokemon_data)

        if not is_pokemon_sum_valid:
            raise serializers.ValidationError("ERROR: Your pokemons sum more than 600 points.")

        pokemons = get_or_create_pokemon(pokemon_data)
        attrs["pokemon_1"] = pokemons[0]
        attrs["pokemon_2"] = pokemons[1]
        attrs["pokemon_3"] = pokemons[2]

        return attrs

    def update(self, instance, validated_data):
        instance.pokemons.clear()
        PokemonTeam.objects.create(
            team=instance,
            pokemon=validated_data["pokemon_1"],
            order=validated_data["pokemon_1_position"],
        )
        PokemonTeam.objects.create(
            team=instance,
            pokemon=validated_data["pokemon_2"],
            order=validated_data["pokemon_2_position"],
        )
        PokemonTeam.objects.create(
            team=instance,
            pokemon=validated_data["pokemon_3"],
            order=validated_data["pokemon_3_position"],
        )

        battle = instance.battle

        creator = (
            Team.objects.filter(battle=battle, trainer=battle.creator)
            .prefetch_related("pokemons")
            .get()
        )
        creator_pokemons = creator.pokemons.all()

        opponent = (
            Team.objects.filter(battle=battle, trainer=battle.opponent)
            .prefetch_related("pokemons")
            .get()
        )
        opponent_pokemons = opponent.pokemons.all()

        if creator_pokemons and opponent_pokemons:
            run_battle_and_send_result_email.delay(battle.id)

        return instance
