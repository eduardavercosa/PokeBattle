from django.urls import path

from battling.views import (
    CreateBattle,
    CreateTeam,
    DeleteBattle,
    DetailBattle,
    Home,
    OnGoingBattles,
    SettledBattles,
)


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("battle/ongoing/", OnGoingBattles.as_view(), name="ongoing_battles"),
    path("battle/settled/", SettledBattles.as_view(), name="settled_battles"),
    path("team/<int:pk>/edit/", CreateTeam.as_view(), name="create_team"),
    path("battle/<int:pk>/delete/", DeleteBattle.as_view(), name="delete_battle"),
    path("battle/<int:pk>/detail/", DetailBattle.as_view(), name="battle_detail"),
]
