from rest_framework import serializers

from battling.models import Battle, PokemonTeam, Team
from pokemon.models import Pokemon
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id")


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ("poke_id", "name", "img_url", "attack", "defense", "hp")


class TeamSerializer(serializers.ModelSerializer):
    pokemon_1 = PokemonSerializer()
    pokemon_2 = PokemonSerializer()
    pokemon_3 = PokemonSerializer()

    class Meta:
        model = PokemonTeam
        fields = ("pokemon_1", "pokemon_2", "pokemon_3")


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner")


class BattleDetailSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    creator_team = serializers.SerializerMethodField()
    opponent = UserSerializer()
    opponent_team = serializers.SerializerMethodField()
    winner = UserSerializer()

    def get_creator_team(self, obj):
        creator_team = Team.objects.filter(battle=obj, trainer=obj.creator).first()
        creator_pokemon_list = PokemonTeam.objects.filter(team=creator_team).first()

        if not creator_team:
            return {}

        creator_serializer = TeamSerializer(instance=creator_pokemon_list)

        return creator_serializer.data

    def get_opponent_team(self, obj):
        opponent_team = Team.objects.filter(battle=obj, trainer=obj.opponent).first()
        opponent_pokemon_list = PokemonTeam.objects.filter(team=opponent_team).first()

        if not opponent_team:
            return {}

        opponent_serializer = TeamSerializer(instance=opponent_pokemon_list)

        return opponent_serializer.data

    def get_winner(self, obj):
        if obj.status == "ONGOING":
            return {}

        winner = obj.winner

        return winner

    class Meta:
        model = Battle
        fields = (
            "creator",
            "creator_team",
            "opponent",
            "opponent_team",
            "winner",
        )
