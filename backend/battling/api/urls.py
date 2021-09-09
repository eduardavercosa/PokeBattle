from django.urls import path

from battling.api import endpoints


urlpatterns = [
    path("api/battles/list/", endpoints.BattleList.as_view(), name="battle-list"),
    path("api/battles/<int:pk>/", endpoints.BattleDetail.as_view(), name="battle-detail"),
    path("api/battles/create/", endpoints.CreateBattle.as_view(), name="create-battle"),
    path("api/team/<int:pk>/edit/", endpoints.CreateTeam.as_view(), name="create-team"),
    path("api/user/", endpoints.CurrentUserEndpoint.as_view(), name="logged-user"),
]
