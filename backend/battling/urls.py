from django.urls import path

from battling.views import BattleList, CreateBattle, CreateTeam, DeleteBattle, DetailBattle, Home


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("battle/list/", BattleList.as_view(), name="battle_list"),
    path("team/<int:pk>/edit/", CreateTeam.as_view(), name="create_team"),
    path("battle/<int:pk>/delete/", DeleteBattle.as_view(), name="delete_battle"),
    path("battle/<int:pk>/detail/", DetailBattle.as_view(), name="battle_detail"),
]
