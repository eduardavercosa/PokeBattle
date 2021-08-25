from django.urls import path

from battling.api import endpoints


urlpatterns = [
    path("battles/list/", endpoints.BattleList.as_view(), name="battle-list"),
    path("battles/<int:pk>/", endpoints.BattleDetail.as_view(), name="battle-detail"),
    path("battles/create/", endpoints.CreateBattle.as_view(), name="create-battle"),
    path("team/<int:pk>/edit/", endpoints.CreateTeam.as_view(), name="team_create"),
    path("user/", endpoints.CurrentUserEndpoint.as_view(), name="current-user"),
]
