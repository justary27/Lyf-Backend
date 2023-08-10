from django.urls import path, include

from . import views

urlpatterns = [
    path('delete/', views.LyfUserViews.delete_account),
    
    path('todo/', include('apps.todo.urls')),
    path('diary/', include('apps.diary.urls')),
]
