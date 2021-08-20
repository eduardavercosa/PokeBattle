from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

import django_js_reverse.views


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path("", include("battling.urls")),
    path("api/", include("battling.api.urls")),
    # React Urls
    path(
        "react/battle/<int:pk>/detail",
        TemplateView.as_view(template_name="react/react_template.html"),
        name="react_template",
    ),
    path(
        "react/battles/list",
        TemplateView.as_view(template_name="react/react_template.html"),
        name="react_template",
    ),
]
