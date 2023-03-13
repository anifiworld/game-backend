from django.urls import path

from . import views

urlpatterns = [
    path("", views.index.as_view()),
    path("health/", views.health.as_view()),
    # path("get_colors/", views.get_colors),
    # path("add_color/", views.add_color),
]
