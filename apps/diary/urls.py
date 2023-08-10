from django.urls import path
from . import views

urlpatterns = [
    path("", views.DiaryViews.diary_list),
    path("<str:entry_id>/", views.DiaryViews.diary_detail),
]
