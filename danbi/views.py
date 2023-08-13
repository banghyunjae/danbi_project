from django.shortcuts import render
from rest_framework import generics, serializers, permissions
from danbi.serializers import TeamSerializer, TaskSerializer, SubTaskSerializer
from danbi.models import Team, Task, SubTask
from django.utils import timezone


# 팀 생성 및 조회를 위한 뷰
class TeamList(generics.ListCreateAPIView):
    """
    - queryset: Team 모델의 모든 객체를 가져옴
    - serializer_class: TeamSerializer를 사용하여 직렬화
    - permission_classes: 인증된 사용자만이 접근 가능
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


# 팀 조회, 수정 및 삭제를 위한 뷰
class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - queryset: Team 모델의 모든 객체를 가져옴
    - serializer_class: TeamSerializer를 사용하여 직렬화
    - permission_classes: 인증된 사용자만이 접근 가능
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


# 업무 생성 및 조회를 위한 뷰
class TaskList(generics.ListCreateAPIView):
    """
    - serializer_class: TaskSerializer를 사용하여 직렬화
    - permission_classes: 인증된 사용자만이 접근 가능
    - get_queryset: 업무를 생성할 때, 하나 이상의 팀이 필요
    - perform_create: 하위 업무가 없거나, 하위 업무의 개수가 0인 경우, 업무 생성이 불가능
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_team = self.request.user.team
        return Task.objects.filter(task_subtasks__team=user_team).order_by("id")

    def perform_create(self, serializer):
        sub_tasks = self.request.data.get("subtask")
        if not sub_tasks or len(sub_tasks) == 0:
            raise serializers.ValidationError("하위업무를 설정해주세요.")

        allowed_teams = Team.objects.values_list("id", flat=True)
        for sub_task in sub_tasks:
            if sub_task["team"] not in allowed_teams:
                raise serializers.ValidationError(f"허용되지 않는 팀 {sub_task['team']}입니다.")
        serializer.save(create_user=self.request.user)


# 업무 조회, 수정 및 삭제를 위한 뷰
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - serializer_class: TaskSerializer를 사용하여 직렬화
    - permission_classes: 인증된 사용자만이 접근 가능
    - get_queryset: 업무를 조회할 때, 해당 업무의 작성자만이 조회 가능
    - perform_update: 업무를 수정할 때, 해당 업무의 작성자만이 수정 가능
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team_subtasks = SubTask.objects.filter(team=self.request.user.team)
        return Task.objects.filter(create_user=self.request.user) | Task.objects.filter(
            task_subtasks__in=team_subtasks
        )

    def perform_update(self, serializer):
        task = self.get_object()
        if task.create_user != self.request.user:
            raise serializers.ValidationError("작성자만 업무를 수정할 수 있습니다.")
        if all(subtask.is_complete for subtask in task.task_subtasks.all()):
            serializer.save(is_complete=True, completed_date=timezone.now())
        else:
            serializer.save()


# 하위업무 생성 및 조회를 위한 뷰
class SubTaskList(generics.ListCreateAPIView):
    """
    - queryset: SubTask 모델의 모든 객체를 가져옴
    - serializer_class: SubTaskSerializer를 사용하여 직렬화
    - permission_classes: 인증된 사용자만이 접근 가능
    """

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated]


# 하위업무 조회, 수정 및 삭제를 위한 뷰
class SubTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - serializer_class: SubTaskSerializer를 사용하여 직렬화
    - permission_classes: 인증된 사용자만이 접근 가능
    - get_queryset: 하위업무를 조회할 때, 해당 하위업무의 소속된 팀만이 조회 가능
    - perform_update: 하위업무를 수정할 때, 해당 하위업무의 소속된 팀만이 수정 가능
    """

    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(team=self.request.user.team)

    def perform_update(self, serializer):
        subtask = self.get_object()
        if subtask.is_complete:
            raise serializers.ValidationError("완료된 하위 업무는 수정할 수 없습니다.")
        if self.request.data.get("is_complete") and subtask.team != self.request.user.team:
            raise serializers.ValidationError("하위업무를 완료 처리할 수 있는 것은 해당 팀만 가능합니다.")
        serializer.save()

    def update(self, request, *args, **kwargs):
        subtask = self.get_object()
        if subtask.is_complete:
            raise serializers.ValidationError("완료된 하위 업무는 삭제할 수 없습니다.")
        return super().update(request, *args, **kwargs)
