from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate  # 인증된 사용자인지 확인하기 위해 사용


from .models import User
from .serializers import SignupSerializer, SigninSerializer


class SignupView(generics.CreateAPIView):
    """
    queryset -> User모델 객체를 모두 가져옴
    serializer_class -> SignupSerializer를 사용
    permission_classes -> 인증되지 않은 사용자도 접근 가능
    """

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class SigninView(generics.CreateAPIView):
    """
    serializer_class -> SigninSerializer를 사용
    permission_classes -> 인증되지 않은 사용자도 접근 가능

    create 메서드를 오버라이딩하여 authenticate를 통해 인증된 사용자인지 확인
    인증된 사용자라면 refresh token을 발급
    """

    serializer_class = SigninSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        return Response({"인증되지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.DestroyAPIView):
    """
    구현 안됨 추후 블랙리스트 모델을 만들어서 구현할 예정
    """

    pass
