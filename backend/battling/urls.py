from django.contrib.auth.views import LogoutView
from django.urls import path

from battling.views import BattleList, CreateBattle, CreateTeam, DeleteBattle, DetailBattle, Home
from users.views import Login, Signup


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", Signup.as_view(), name="signup"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("battle/list/", BattleList.as_view(), name="battle_list"),
    path("team/<int:pk>/edit/", CreateTeam.as_view(), name="create_team"),
    path("battle/<int:pk>/delete/", DeleteBattle.as_view(), name="delete_battle"),
    path("battle/<int:pk>/detail/", DetailBattle.as_view(), name="battle_detail"),
]
