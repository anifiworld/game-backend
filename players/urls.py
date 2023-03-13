from django.urls import path

from . import views

urlpatterns = [
    path("info/", views.PlayerDetail.as_view()),
    path("get_free_heroes/", views.GetFreeHeroes.as_view()),
    #path("get_claim/<id>", views.GetClaim.as_view()),
    path("claim_reward/", views.ClaimReward.as_view()),
]
