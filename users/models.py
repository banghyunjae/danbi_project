from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    BaseUserManager를 상속받아서 커스텀 User를 생성
    현재 UserManager는 create_user와 create_superuser 메서드를 오버라이딩해서 사용하고 있음
    """

    def create_user(
        self, username, team, pw=None
    ):  # create_user메서드는 현재 username, team, pw를 받아서 User를 생성
        if not username:
            raise ValueError("이름을 입력해주세요.")
        if not team:
            raise ValueError("팀을 입력해주세요.")
        user = self.model(
            username=username,
            team=team,
        )
        user.set_password(pw)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, team, pw
    ):  # create_superuser메서드는 현재 username, team, pw를 받아서 관리자 생성
        user = self.create_user(
            username=username,
            team=team,
            pw=pw,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    AbstractBaseUser를 상속받아서 커스텀 User를 생성
    User 모델은 username, team, is_admin, is_staff, is_active 필드를 가지고 있음
    """

    username = models.CharField(max_length=50, unique=True)
    team = models.ForeignKey("danbi.Team", on_delete=models.CASCADE, related_name="team_users")

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = "username"  # USERNAME_FIELD는 username을 사용하겠다는 의미
    REQUIRED_FIELDS = ["team"]  # REQUIRED_FIELDS는 필수로 입력받을 필드를 의미

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
