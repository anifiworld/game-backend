from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index),
    # path("health/", views.health),
    # path("get_colors/", views.get_colors),
    # path("add_color/", views.add_color),
    path("user/item_list/", views.ItemList.as_view()),
    path("item_shop/", views.ItemShopList.as_view()),
    path("buy_item/", views.BuyItem.as_view()),
]
