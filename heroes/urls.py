from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListCreateAPIView

from . import views

urlpatterns = [
    # path("", views.index),
    # path("hero/", views.health),
    path("types/", views.HeroList.as_view()),
    path("gems/", views.GemsList.as_view()),
    path("user/hero_list/", views.HeroUserList.as_view()),
    # path("user/hero_on_chain_list/", views.HeroOnChainList.as_view()),
    # path("user/mock_list/", views.HeroUserMockList.as_view()),
    # path("user/mock_nft_list/", views.HeroUserNftMockList.as_view()),
    path("user/hero_slots/", views.HeroSlots.as_view()),
    path("user/gem_slots/<str:hero_nft>", views.GemSlotsList.as_view()),
    path("user/gem_list/", views.GemUserList.as_view()),
    path("user/gem_buy/", views.GemBuy.as_view()),
    # path("user/sync/", cache_page(5)(views.sync_items)),
    path("user/hero_card/<str:nft_id>", views.HeroCard.as_view()),
]
