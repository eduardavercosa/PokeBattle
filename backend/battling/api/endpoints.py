from django.db.models import Q

from rest_framework import generics, permissions

from battling.api.serializers import BattleSerializer
from battling.models import Battle


class BattleList(generics.ListAPIView):

    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by("-id")
        return queryset
