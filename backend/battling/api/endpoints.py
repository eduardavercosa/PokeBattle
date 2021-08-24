from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from battling.api.serializers import BattleSerializer, CreateTeamSerializer, UserSerializer
from battling.models import Battle, Team


class CurrentUserEndpoint(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class BattleList(generics.ListCreateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by("-id")
        return queryset


class BattleDetail(generics.RetrieveAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by("-id")
        return queryset


class CreateBattle(generics.CreateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateTeam(generics.UpdateAPIView):
    serializer_class = CreateTeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Team.objects.filter(trainer=self.request.user)
        return queryset
