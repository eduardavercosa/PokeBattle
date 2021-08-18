from rest_framework import serializers

from battling.models import Battle, PokemonTeam, Team
from battling.tasks import run_battle_and_send_result_email
from pokemon.helpers import _has_both_teams, has_repeated_pokemon, is_team_valid
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


class BattleSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
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
            "status",
            "creator",
            "creator_id",
            "opponent",
            "opponent_id",
            "teams",
            "status",
            "winner",
        )

    def validate(self, attrs):
        if attrs["creator"] == attrs["opponent"]:
            raise serializers.ValidationError("ERROR: You can't challenge yourself.")

        return attrs

    def create(self, validated_data):
        validated_data["creator"] = self.context.get("request").user
        instance = super().create(validated_data)

        set_up_battle_teams_and_send_invite_email(instance)
        return instance


class CreateTeamSerializer(serializers.ModelSerializer):
    pokemons_ids = serializers.PrimaryKeyRelatedField(
        source="pokemons",
        queryset=Pokemon.objects.all(),
        many=True,
    )

    class Meta:
        model = PokemonTeam
        fields = (
            "id",
            "pokemons_ids",
        )

    def validate(self, attrs):
        pokemon_list = attrs["pokemons"]
        if len(pokemon_list) != 3:
            raise serializers.ValidationError("ERROR: All fields are required.")

        team_has_repeated_pokemon = has_repeated_pokemon(pokemon_list)
        if team_has_repeated_pokemon:
            raise serializers.ValidationError("You can't choose the same Pokemon more than once.")

        is_pokemon_sum_valid = is_team_valid(pokemon_list)

        if not is_pokemon_sum_valid:
            raise serializers.ValidationError("ERROR: Your pokemons sum more than 600 points.")

        return attrs

    def update(self, instance, validated_data):
        instance.pokemons.clear()
        PokemonTeam.objects.create(
            team=instance,
            pokemon=validated_data["pokemons"][0],
            order=1,
        )
        PokemonTeam.objects.create(
            team=instance,
            pokemon=validated_data["pokemons"][1],
            order=2,
        )
        PokemonTeam.objects.create(
            team=instance,
            pokemon=validated_data["pokemons"][2],
            order=3,
        )

        battle = instance.battle

        if _has_both_teams(battle):
            run_battle_and_send_result_email.delay(battle.id)

        return instance
