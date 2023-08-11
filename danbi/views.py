from django.shortcuts import render
from rest_framework import generics
from .serializers import TeamSerializer, UserSerializer, TaskSerializer, SubTaskSerializer
from .models import Team, User, Task, SubTask


class TeamList(generics.ListCreateAPIView):  # 팀 생성, 팀 조회
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):  # 팀 조회, 수정, 팀 삭제
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserList(generics.ListCreateRetrieveUpdateDestroyAPIView):  # 유저 생성, 유저 조회, 유저 수정, 유저 삭제
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskList(generics.ListCreateAPIView):  # 업무 생성, 업무 조회
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):  # 팀원이 속한 팀의 업무만 조회
        user_team = self.request.user.team
        return Team.objects.filter(name=user_team)

    def perform_create(self, serializer):  # 업무 생성 시, 작성자는 팀원만 가능
        serializer.save(create_user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):  # 업무 조회, 업무 수정, 업무 삭제
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # 업무를 수정할 수 있는 사람은 작성자
    # 기존 하위 업무들 중 완료된 것은 삭제 불가
    # 모든 하위 업무가 완료되면 상위 업무도 완료


class SubTaskList(generics.ListCreateAPIView):  # 하위업무 생성, 하위업무 조회
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class SubTaskDetail(generics.RetrieveUpdateDestroyAPIView):  # 하위업무 조회, 하위업무 수정, 하위업무 삭제
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    # 하위업무 완료 처리는 해당 팀만 할 수 있음
