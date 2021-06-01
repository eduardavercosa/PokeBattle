from django.urls import path

from battling.views import CreateBattle, CreateTeam, DeleteTeam, DetailBattle, Home


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("team/<int:pk>/edit/", CreateTeam.as_view(), name="create_team"),
    path("team/<int:pk>/delete/", DeleteTeam.as_view(), name="delete_team"),
    path("battle/<int:pk>/detail/", DetailBattle.as_view(), name="battle_details"),
]
