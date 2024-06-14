from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('add/', views.create_task, name='create_task'),
    path('kanban/', views.kanban, name='kanban'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
