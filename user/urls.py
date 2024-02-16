from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LyfUserViews.login),
    path('delete/', views.LyfUserViews.delete_account),

    path('<str:user_id>/todo/', include('apps.todo.urls')),
    path('<str:user_id>/diary/', include('apps.diary.urls')),
]
