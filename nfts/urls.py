from django.urls import path

from . import views

urlpatterns = [
    path("meta/<str:nft_id>", views.NFTMetaData.as_view()),
]
