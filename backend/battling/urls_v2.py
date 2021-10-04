from django.conf.urls import include, url  # noqa
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        "battle/<int:pk>/detail",
        TemplateView.as_view(template_name="react/spa_template.html"),
        name="battle_detail_v2",
    ),
    path(
        "battle/list",
        TemplateView.as_view(template_name="react/spa_template.html"),
        name="battle_list_v2",
    ),
    path(
        "battle/create",
        TemplateView.as_view(template_name="react/spa_template.html"),
        name="battle_create_v2",
    ),
    path(
        "team/<int:pk>/edit",
        TemplateView.as_view(template_name="react/spa_template.html"),
        name="team_create_v2",
    ),
]
