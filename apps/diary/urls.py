from django.urls import path
from .views import DiaryViews

urlpatterns = [
    path("", DiaryViews.diary_list),
    path("<uuid:entry_id>/", DiaryViews.diary_detail),
]
