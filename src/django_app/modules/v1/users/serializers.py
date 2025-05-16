# django_app/modules/v1/users/serializers.py

from rest_framework import serializers
from .models import User

class UserIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class UserCreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

class UserUpdateRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def validate_email(self, value):
        if User.objects.exclude(id=self.initial_data.get('id')).filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.exclude(id=self.initial_data.get('id')).filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

class PaginationRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    per_page = serializers.IntegerField(required=False, default=10)
    sort = serializers.CharField(required=False, default='id')
    sort_dir = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')

class UserSearchRequestSerializer(PaginationRequestSerializer):
    query = serializers.CharField()
    field = serializers.ChoiceField(choices=['username', 'email', 'first_name', 'last_name'])

class UserFilterRequestSerializer(PaginationRequestSerializer):
    uuid = serializers.UUIDField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')

class UserCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserExistsResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    exists = serializers.BooleanField()

class PaginationResponseSerializer(serializers.Serializer):
    items = serializers.ListField()
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()

# serializers.py
class UserQuerySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    uuid = serializers.UUIDField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)