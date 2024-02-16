from django.urls import path
from .views import TodoViews

urlpatterns = [
    path("", TodoViews.todo_list),
    path("<uuid:todo_id>/", TodoViews.todo_detail),
]
