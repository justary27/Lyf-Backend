from django.urls import path
from .views import DiaryViews

urlpatterns = [
    path("", DiaryViews.diary_list),
    path("<uuid:entry_id>/", DiaryViews.diary_detail),

    path("pdf/", DiaryViews.get_diary_as_pdf),
    path("txt/", DiaryViews.get_diary_as_txt),

    path("<uuid:entry_id>/pdf/", DiaryViews.get_entry_as_pdf),
    path("<uuid:entry_id>/txt/", DiaryViews.get_entry_as_txt),
]
