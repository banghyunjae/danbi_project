from rest_framework import serializers
from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    """
    signup 시리얼라이저
    password를 write_only로 설정하여 응답에 포함되지 않도록 함
    create 메소드는 username, team, password를 받아서 User 객체를 생성하고 저장
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "team", "password"]

    def create(self, validated_data):
        user = User(username=validated_data["username"], team=validated_data["team"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class SigninSerializer(serializers.Serializer):
    """
    signin 시리얼라이저
    username, password를 받아서 인증된 사용자인지 확인
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
