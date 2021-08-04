from django.urls import path

from battling.api import endpoints


urlpatterns = [
    path("battles/", endpoints.BattleList.as_view(), name="battle-list"),
]
