from rest_framework import serializers

from battling.models import Battle, Team
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
    pokemons = PokemonSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "battle", "trainer", "pokemons")


class BattleSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
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
        fields = ("id", "creator", "creator_id", "opponent", "opponent_id", "teams", "winner")

    def create(self, validated_data):
        validated_data["creator"] = self.context.get("request").user
        instance = super().create(validated_data)

        set_up_battle_teams_and_send_invite_email(instance)
        return instance
