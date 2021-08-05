from django.urls import path

from battling.api import endpoints


urlpatterns = [
    path("battles/list/", endpoints.BattleList.as_view(), name="battle-list"),
    path("battles/<int:pk>/", endpoints.BattleDetail.as_view(), name="battle-detail"),
    path("battles/create/", endpoints.CreateBattle.as_view(), name="create-battle"),
]
