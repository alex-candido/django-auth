# django_app/modules/v1/users/api.py

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .services import UserService
from .serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserSearchSerializer,
    UserFilterSerializer,
    UserSerializer
)

user_service = UserService()

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user actions."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer 

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def find_one(self, request):
        result = user_service.find_one(request.query_params)
        if result:
            return Response(result, status=status.HTTP_200_OK)  
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def find_all(self, request):
        result = user_service.find_all()
        return Response(UserSerializer(result, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_one(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = user_service.create_one(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_many(self, request):
        serializer = UserCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            result = user_service.create_many(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_one(self, request):
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            result = user_service.update_one(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_many(self, request):
        serializer = UserUpdateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            result = user_service.update_many(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_one(self, request):
        result = user_service.remove_one(request.query_params)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_many(self, request):
        result = user_service.remove_many(request.query_params)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def search(self, request):
        serializer = UserSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            result = user_service.search(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def filter(self, request):
        serializer = UserFilterSerializer(data=request.query_params)
        if serializer.is_valid():
            result = user_service.filter(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def find_by_id(self, request):
        result = user_service.find_by_id(request.query_params.get('id'))
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def find_by_ids(self, request):
        result = user_service.find_by_ids(request.query_params.getlist('ids[]'))
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def exists_by_id(self, request):
        result = user_service.exists_by_id(request.query_params.get('id'))
        return Response({'exists': result}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def exists_by_ids(self, request):
        result = user_service.exists_by_ids(request.query_params.getlist('ids[]'))
        return Response({'exists': result}, status=status.HTTP_200_OK)

