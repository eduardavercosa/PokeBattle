from django.conf.urls import include
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from battling.views import (
    BattleListView,
    CreateBattleView,
    CreateTeamView,
    DeleteBattleView,
    DetailBattleView,
    HomeView,
)
from users.views import LoginView, SignupView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/login/", LoginView.as_view(), name="login"),
    path("account/logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("account/signup/", SignupView.as_view(), name="signup"),
    path("battle/new/", CreateBattleView.as_view(), name="create_battle"),
    path("battle/list/", BattleListView.as_view(), name="battle_list"),
    path("team/<int:pk>/edit/", CreateTeamView.as_view(), name="create_team"),
    path("battle/<int:pk>/delete/", DeleteBattleView.as_view(), name="delete_battle"),
    path("battle/<int:pk>/detail/", DetailBattleView.as_view(), name="battle_detail"),
    path("oauth/", include("social_django.urls"), name="social"),
    # Signup urls
    path(
        "signup/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="registration/signup_confirm.html",
            success_url=reverse_lazy("signup_complete"),
        ),
        name="signup_confirm",
    ),
    path(
        "signup/done/",
        views.PasswordResetCompleteView.as_view(template_name="registration/signup_complete.html"),
        name="signup_complete",
    ),
]
