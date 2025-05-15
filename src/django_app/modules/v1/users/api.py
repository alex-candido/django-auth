# django_app/modules/v1/users/api.py

from ast import List
from pydot import Any
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer
)

from .use_cases import FindOneUseCase
from .repositories import UserRepository

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

# validated_data, _to_response, _list_response

class UserViewSet(viewsets.ModelViewSet):  
    find_one_use_case = FindOneUseCase(repository=UserRepository())
    find_all_use_case = FindAllUseCase(repository=UserRepository())
    create_one_use_case = CreateOneUseCase(repository=UserRepository())
    create_many_use_case = CreateManyUseCase(repository=UserRepository())
    update_one_use_case = UpdateOneUseCase(repository=UserRepository())
    update_many_use_case = UpdateManyUseCase(repository=UserRepository())
    remove_one_use_case = RemoveOneUseCase(repository=UserRepository())
    remove_many_use_case = RemoveManyUseCase(repository=UserRepository())
    search_use_case = SearchUseCase(repository=UserRepository())
    filter_use_case = FilterUseCase(repository=UserRepository())
    find_by_id_use_case = FindByIdUseCase(repository=UserRepository())
    find_by_ids_use_case = FindByIdsUseCase(repository=UserRepository())
    exists_by_id_use_case = ExistsByIdUseCase(repository=UserRepository())
    exists_by_ids_use_case = ExistsByIdsUseCase(repository=UserRepository())


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def find_one(self, request):
        validated_data = self._validated_data(UserSerializer, request.query_params)
        input_param = self.find_one_use_case.Input(**validated_data)
        output = self.find_one_use_case.execute(input_param)
        data = self.to_response(UserSerializer, output)
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def find_all(self, request):
        output = self.find_all_use_case.execute()
        data = self._list_response(UserSerializer, output)
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def create_one(self, request):
        validated_data = self._validated_data(UserCreateRequestSerializer, request.data)
        input_data = self.create_one_use_case.Input(**validated_data)
        output = self.create_one_use_case.execute(input_data)
        data = self._to_response(UserCreateResponseSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def create_many(self, request):
        validated_data = self._validated_data(UserCreateRequestSerializer, request.data, many=True)
        input_data = self.create_many_use_case.Input(users=validated_data)
        output = self.create_many_use_case.execute(input_data)
        data = self._list_response(UserCreateResponseSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    def update_one(self, request):
        validated_data = self._validated_data(UserUpdateRequestSerializer, request.data)
        input_data = self.update_one_use_case.Input(**validated_data)
        output = self.update_one_use_case.execute(input_data)
        data = self._to_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    def update_many(self, request):
        validated_data = self._validated_data(UserUpdateRequestSerializer, request.data, many=True)
        input_data = self.update_many_use_case.Input(users=validated_data)
        output = self.update_many_use_case.execute(input_data)
        data = self._list_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    def remove_one(self, request):
        validated_data = self._validated_data(UserDeleteRequestSerializer, request.data)
        input_data = self.remove_one_use_case.Input(**validated_data)
        self.remove_one_use_case.execute(input_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    def remove_many(self, request):
        validated_data = self._validated_data(UserDeleteRequestSerializer, request.data, many=True)
        input_data = self.remove_many_use_case.Input(users=validated_data)
        self.remove_many_use_case.execute(input_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # --- Extras ---
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def search(self, request):
        validated_data = self._validated_data(UserSearchRequestSerializer, request.query_params)
        input_data = self.search_use_case.Input(**validated_data)
        output = self.search_use_case.execute(input_data)
        data = self._list_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def filter(self, request):
        validated_data = self._validated_data(UserFilterRequestSerializer, request.query_params)
        input_data = self.filter_use_case.Input(**validated_data)
        output = self.filter_use_case.execute(input_data)
        data = self._list_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def find_by_id(self, request):
        validated_data = self._validated_data(UserFindByIdRequestSerializer, request.query_params)
        input_data = self.find_by_id_use_case.Input(**validated_data)
        output = self.find_by_id_use_case.execute(input_data)
        data = self._to_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def find_by_ids(self, request):
        validated_data = self._validated_data(UserFindByIdsRequestSerializer, request.query_params)
        input_data = self.find_by_ids_use_case.Input(**validated_data)
        output = self.find_by_ids_use_case.execute(input_data)
        data = self._list_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def exists_by_id(self, request):
        validated_data = self._validated_data(UserExistsByIdRequestSerializer, request.query_params)
        input_data = self.exists_by_id_use_case.Input(**validated_data)
        output = self.exists_by_id_use_case.execute(input_data)
        return Response({'exists': output.exists}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def exists_by_ids(self, request):
        validated_data = self._validated_data(UserExistsByIdsRequestSerializer, request.query_params)
        input_data = self.exists_by_ids_use_case.Input(**validated_data)
        output = self.exists_by_ids_use_case.execute(input_data)
        return Response({'exists': output.exists}, status=status.HTTP_200_OK)
    
    # --- Utils ---
    
    @staticmethod
    def _validated_data(serializer_class: Serializer, data: dict) -> dict:
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _to_response(serializer_class: Serializer, output: Any) -> dict:
        serializer = serializer_class(data=output)
        return serializer.data
    
    def _list_response(self, serializer_class: Serializer, output: List[Any]) -> List[dict]:
        serializer = serializer_class(data=output, many=True)
        return serializer.data
    