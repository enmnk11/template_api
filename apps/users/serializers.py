from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'tokens')

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tokens'] = self.get_tokens(instance)
        return data

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = '__all__'