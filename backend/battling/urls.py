from django.urls import path

from battling.views import CreateBattle, DetailBattle, EnterBattle, Home


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/new/", CreateBattle.as_view(), name="create_battle"),
    path("battle/<int:pk>/team/", EnterBattle.as_view(), name="enter_battle"),
    path("battle/<int:pk>/details/", DetailBattle.as_view(), name="battle_details"),
]
