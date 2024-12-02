from django.urls import path
from .views import \
    ProjectListCreateView, ProjectListUpdateDeleteView, \
    TaskProjectListCreateView, TaskListUpdateDeleteView, \
    SubtaskListCreateView, SubtaskUpdateDeleteView

app_name = 'projects'

urlpatterns = [
    
    # Project
    path('list/create/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('update/destroy/<int:pk>/', ProjectListUpdateDeleteView.as_view(), name='update_destroy_project'),
    
    # Task
    path('task/<int:pk>/', TaskProjectListCreateView.as_view(), name='create_list_task_project'),
    path('task/update/destroy/<int:pk>/', TaskListUpdateDeleteView.as_view(), name='update_destroy_task'),
    
    # Subtask
    path('subtask/<int:pk>/', SubtaskListCreateView.as_view(), name='create_list_subtask_project'),
    path('subtask/update/destroy/<int:pk>/', SubtaskUpdateDeleteView.as_view(), name='update_destroy_subtask'),
]
