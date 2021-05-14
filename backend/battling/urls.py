from django.urls import path

from battling.views import CreateBattle, CreateTeam, DetailBattle, Home, JoinBattle


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("team/<int:pk>/edit/", CreateTeam.as_view(), name="create_team"),
    path("battle/<int:pk>/join/", JoinBattle.as_view(), name="join_battle"),
    path("battle/<int:pk>/details/", DetailBattle.as_view(), name="battle_details"),
]
