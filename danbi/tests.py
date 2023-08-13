from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from users.models import User
from danbi.models import Team, Task, SubTask


class TestTask(APITestCase):
    """
    setUp -> 팀 생성, 사용자 생성, 로그인
    """

    def setUp(self) -> None:
        self.team1 = Team.objects.create(name="단비")
        self.team2 = Team.objects.create(name="다래")
        self.team3 = Team.objects.create(name="블라블라")
        self.team4 = Team.objects.create(name="철로")
        self.team6 = Team.objects.create(name="땅이")
        self.team5 = Team.objects.create(name="해태")
        self.team7 = Team.objects.create(name="수피")

        self.user1 = User.objects.create_user(
            username="hyunjae",
            team=self.team1,
        )
        self.user1.set_password("1234")
        self.user1.save()

        self.signin_url = reverse("users:signin")
        self.task_list_create_url = reverse("danbi:task_list")
        self.task_detail_url = reverse("danbi:task_detail", kwargs={"pk": 1})
        self.subtask_list_create_url = reverse("danbi:subtask_list")
        self.subtask_detail_url = reverse("danbi:subtask_detail", kwargs={"pk": 1})

        response = self.client.post(
            self.signin_url,
            data={"username": "hyunjae", "password": "1234"},
            format="json",
        )
        self.token = response.data["access_token"]

    def tearDown(self) -> None:
        """
        업무, 하위업무 모두 삭제
        """
        Task.objects.all().delete()
        SubTask.objects.all().delete()

        super().tearDown()

    # -----------------------업무 생성 테스트-----------------------#
    def test_task_create(self):
        data = {
            "title": "테스트 업무 3번",
            "content": "테스트 업무 3번에 대한 설명입니다.",
            "team": self.team1.id,
            "create_user": self.user1.id,
            "subtask": [
                {"team": self.team1.id},
                {"team": self.team2.id},
            ],
        }

        response = self.client.post(
            self.task_list_create_url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    # -----------------------업무 생성 실패 테스트-----------------------#
    def test_task_create_fail(self):
        data = {
            "title": "테스트 업무 3번",
            "content": "테스트 업무 3번에 대한 설명입니다.",
            "team": self.team1.id,
            "create_user": self.user1.id,
            "subtask": [],
        }

        response = self.client.post(
            self.task_list_create_url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    # -----------------------업무 조회 테스트-----------------------#
    def test_task_list(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        SubTask.objects.create(team=self.team1, task=task, is_complete=False)
        response = self.client.get(
            self.task_list_create_url,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    # -----------------------업무 상세 조회 테스트-----------------------#
    def test_task_detail(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        SubTask.objects.create(team=self.team1, task=task, is_complete=False)
        response = self.client.get(
            self.task_detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------업무 수정 테스트-----------------------#
    def test_task_update(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        SubTask.objects.create(team=self.team1, task=task, is_complete=False)

        data = {
            "title": "테스트 업무 1번 수정",
            "content": "테스트 업무 1번에 대한 설명입니다. 수정",
            "team": self.team1.id,
            "create_user": self.user1.id,
            "task_subtask": [
                {"team": self.team1.id},
                {"team": self.team2.id},
            ],
        }

        response = self.client.put(
            self.task_detail_url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------업무 삭제 테스트-----------------------#
    def test_task_delete(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        SubTask.objects.create(team=self.team1, task=task, is_complete=False)

        response = self.client.delete(
            self.task_detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # -----------------------하위업무 생성 테스트-----------------------#
    def test_subtask_create(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        data = {
            "team": self.team1.id,
            "task": task.id,
        }

        response = self.client.post(
            self.subtask_list_create_url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTask.objects.count(), 1)

    # -----------------------하위업무 조회 테스트-----------------------#
    def test_subtask_list(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        SubTask.objects.create(team=self.team1, task=task, is_complete=False)
        response = self.client.get(
            self.subtask_list_create_url,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    # -----------------------하위업무 상세 조회 테스트-----------------------#
    def test_subtask_detail(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        subtask = SubTask.objects.create(team=self.team1, task=task, is_complete=False)
        response = self.client.get(
            self.subtask_detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------하위업무 수정 테스트-----------------------#
    def test_subtask_update(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        subtask = SubTask.objects.create(team=self.team1, task=task, is_complete=False)

        data = {
            "team": self.team1.id,
            "task": task.id,
            "is_complete": True,
        }

        response = self.client.put(
            self.subtask_detail_url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------하위업무 삭제 테스트-----------------------#
    def test_subtask_delete(self):
        task = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title="테스트 업무 1번",
            content="테스트 업무 1번에 대한 설명입니다.",
        )

        subtask = SubTask.objects.create(team=self.team1, task=task, is_complete=False)

        response = self.client.delete(
            self.subtask_detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
