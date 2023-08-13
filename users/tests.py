from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from danbi.models import Team
from users.models import User


# ------------------------------- 회원 인증 테스트 ------------------------------- #
class UserAuthTest(APITestCase):
    def setUp(self):  # 테스트 시작 전에 실행되는 코드
        self.signup_url = reverse("users:signup")
        self.login_url = reverse("users:signin")
        self.logout_url = reverse("users:logout")

        self.team = Team.objects.create(name="단비")

        self.api_request_data = {
            "username": "helloid",
            "team": self.team.id,
            "password": "1234",
        }

    def tearDown(self):  # 테스트 종료 후에 실행되는 코드 (데이터베이스 정리시 사용)
        user = User.objects.filter(username=self.api_request_data["username"]).first()
        if user:
            user.delete()

    # ------------------------------- 회원 가입 테스트 ------------------------------- #
    def test_signup(self):
        response = self.client.post(self.signup_url, self.api_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.api_request_data["username"]).exists())

    def test_signup_fail(self):
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------------- 로그인 테스트 -------------------------------- #
    def test_login(self):
        # 먼저 회원가입을 통해 사용자 생성
        self.client.post(self.signup_url, self.api_request_data)

        # 로그인 테스트
        response = self.client.post(
            self.login_url,
            {
                "username": self.api_request_data["username"],
                "password": self.api_request_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_login_fail(self):
        self.client.post(self.signup_url, self.api_request_data)

        # 로그인 실패 테스트
        response = self.client.post(
            self.login_url,
            {
                "username": self.api_request_data["username"],
                "password": "wrong_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
