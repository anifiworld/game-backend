from django.urls import path

from . import views

urlpatterns = [
    path("play_stage/", views.PlayStage.as_view()),
    path("cancel_stage/", views.CancelStage.as_view()),
    path("stage_list/", views.StageList.as_view()),
    path("phase_data/<int:pk>", views.PhaseData.as_view()),
    path("stage_data/<int:pk>", views.StageData.as_view()),
]
