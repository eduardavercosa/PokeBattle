from django.urls import path

from battling.views import CreateBattle, CreateTeam, DetailBattle, EditBattle, Home


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("team/<int:pk>/edit/", CreateTeam.as_view(), name="create_team"),
    path("battle/<int:pk>/edit/", EditBattle.as_view(), name="edit_battle"),
    path("battle/<int:pk>/detail/", DetailBattle.as_view(), name="battle_details"),
]
