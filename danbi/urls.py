from danbi import views
from django.urls import path

app_name = "danbi"

urlpatterns = [
    path("teams/", views.TeamList.as_view(), name="team_list"),
    path("teams/<int:pk>/", views.TeamDetail.as_view(), name="team_detail"),
    path("tasks/", views.TaskList.as_view(), name="task_list"),
    path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
    path("subtasks/", views.SubTaskList.as_view(), name="subtask_list"),
    path("subtasks/<int:pk>/", views.SubTaskDetail.as_view(), name="subtask_detail"),
]
