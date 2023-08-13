from django.db import models
from users.models import User


class Team(models.Model):  # Team 모델 단비, 다래, 블라블라, 철로, 땅이, 해태, 수피
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):  # Task 모델 팀명, 업무명, 업무내용, 완료여부, 완료일자, 생성일자, 수정일자
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tasks")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_tasks")
    title = models.CharField(max_length=30)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class SubTask(models.Model):  # SubTask 모델 팀명, 업무명, 완료여부, 완료일자, 생성일자, 수정일자
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_subtasks")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_subtasks")
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
