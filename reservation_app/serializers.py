from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserPublicSerializer(serializers.ModelSerializer):
    """
    This serializer is a public serializer
    """
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class UserAdminSerializer(serializers.ModelSerializer):
    """
    This serializer is for Users with admin permission
    """
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


