# django_app/modules/v1/users/serializers.py

from rest_framework import serializers
from django_app.modules.v1.users.models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Corrige o armazenamento da senha
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_email(self, value):
        user = User.objects.exclude(id=self.initial_data.get('id')).filter(email=value)
        if user.exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_username(self, value):
        user = User.objects.exclude(id=self.initial_data.get('id')).filter(username=value)
        if user.exists():
            raise serializers.ValidationError('Username already exists')
        return value

class UserSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    field = serializers.ChoiceField(
        choices=['username', 'email', 'first_name', 'last_name'],
        required=True
    )

class UserFilterSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=['admin', 'user'],
        required=False
    )
    status = serializers.ChoiceField(
        choices=['active', 'inactive'],
        required=False
    )

class UserSerializer(serializers.ModelSerializer):
    """Serializer para representar os dados de um usuário."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')
        read_only_fields = ('id', 'date_joined', 'last_login')  # Campos somente leitura
