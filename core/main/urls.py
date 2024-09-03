from django.urls import path

from . import views

urlpatterns = [
    path("", views.AboutView.as_view(), name='about'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path("login/", views.LoginView.as_view(), name='login'),
    path('update/<int:task_id>/', views.UpdateView.as_view(), name='update')
]