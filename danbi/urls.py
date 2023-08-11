from danbi import views
from django.urls import path

app_name = "danbi"

urlpatterns = [
    # Team
    path("teams/", views.TeamList.as_view(), name="team_list"),
    path("teams/<int:pk>/", views.TeamDetail.as_view(), name="team_detail"),
    # User
    path("users/", views.UserList.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserList.as_view(), name="user_detail"),
    # Task
    path("tasks/", views.TaskList.as_view(), name="task_list"),
    path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
    # SubTask
    path("subtasks/", views.SubTaskList.as_view(), name="subtask_list"),
    path("subtasks/<int:pk>/", views.SubTaskDetail.as_view(), name="subtask_detail"),
]
