from django.urls import path
from . import views

urlpatterns = [
    path("", views.TodoViews.todo_list),
    path("<str:todo_id>/", views.TodoViews.todo_detail),
]
