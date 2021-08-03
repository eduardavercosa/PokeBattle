from django.urls import path

from api.battles import endpoints


urlpatterns = [
    path("battles/ongoing/", endpoints.OngoingBattleList.as_view(), name="ongoing-battle-list"),
    path("battles/settled/", endpoints.SettledBattleList.as_view(), name="settled-battle-list"),
]
