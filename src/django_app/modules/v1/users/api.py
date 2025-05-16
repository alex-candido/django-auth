# django_app/modules/v1/users/api.py

from dataclasses import asdict
from typing import List, Type, Union, Any
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from dependency_injector.wiring import inject, Provide
from django_app.container import container 
from .serializers import (
    PaginationRequestSerializer,
    PaginationResponseSerializer,
    UserCreateRequestSerializer,
    UserCreateResponseSerializer,
    UserExistsResponseSerializer,
    UserFilterRequestSerializer,
    UserResponseSerializer,
    UserSearchRequestSerializer,
    UserUpdateRequestSerializer,
    UserIdSerializer,
    UserQuerySerializer
)

from .use_cases import (
    FindOneUseCase,
    FindAllUseCase,
    CreateOneUseCase,
    CreateManyUseCase,
    UpdateOneUseCase,
    UpdateManyUseCase,
    RemoveOneUseCase,
    RemoveManyUseCase,
    SearchUseCase,
    FilterUseCase,
    FindByIdUseCase,
    FindByIdsUseCase,
    ExistsByIdUseCase,
    ExistsByIdsUseCase,
)

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids, validated_data, _to_response

class UserViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    @inject
    def find_one(self, request, find_one_use_case: FindOneUseCase = Provide[container.users.find_one_use_case]):
        validated_data = self._validated_data(UserQuerySerializer, data=request.query_params)
        # input_param = find_one_use_case.Input(**validated_data)
        use_case_instance = find_one_use_case

        print(use_case_instance.Input)
        # output = find_one_use_case.execute(input_param)
        # data = self._to_response(UserResponseSerializer, output)
        return Response(validated_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @inject
    def find_all(self, request, find_all_use_case: FindAllUseCase = Provide[container.users.find_all_use_case]):
        validated_data = self._validated_data(PaginationRequestSerializer, request.query_params)
        input_param = find_all_use_case.Input(**validated_data)
        output = find_all_use_case.execute(input_param)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    @inject
    def create_one(self, request, create_one_use_case: CreateOneUseCase = Provide[container.users.create_one_use_case]):
        validated_data = self._validated_data(UserCreateRequestSerializer, request.data)
        input_data = create_one_use_case.Input(**validated_data)
        output = create_one_use_case.execute(input_data)
        data = self._to_response(UserCreateResponseSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    @inject
    def create_many(self, request, create_many_use_case: CreateManyUseCase = Provide[container.users.create_many_use_case]):
        validated_data = self._validated_data(UserCreateRequestSerializer, request.data, many=True)
        input_data = create_many_use_case.Input(users=validated_data)
        output = create_many_use_case.execute(input_data)
        data = self._to_response(UserCreateResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    @inject
    def update_one(self, request, update_one_use_case: UpdateOneUseCase = Provide[container.users.update_one_use_case]):
        validated_data = self._validated_data(UserUpdateRequestSerializer, request.data)
        input_data = update_one_use_case.Input(**validated_data)
        output = update_one_use_case.execute(input_data)
        data = self._to_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    @inject
    def update_many(self, request, update_many_use_case: UpdateManyUseCase = Provide[container.users.update_many_use_case]):
        validated_data = self._validated_data(UserUpdateRequestSerializer, request.data, many=True)
        input_data = update_many_use_case.Input(users=validated_data)
        output = update_many_use_case.execute(input_data)
        data = self._to_response(UserResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    @inject
    def remove_one(self, request, remove_one_use_case: RemoveOneUseCase = Provide[container.users.remove_one_use_case]):
        validated_data = self._validated_data(UserIdSerializer, request.data)
        input_data = remove_one_use_case.Input(**validated_data)
        remove_one_use_case.execute(input_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    @inject
    def remove_many(self, request, remove_many_use_case: RemoveManyUseCase = Provide[container.users.remove_many_use_case]):
        validated_data = self._validated_data(UserIdSerializer, request.data, many=True)
        input_data = remove_many_use_case.Input(**validated_data)
        remove_many_use_case.execute(input_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def search(self, request, search_use_case: SearchUseCase = Provide[container.users.search_use_case]):
        validated_data = self._validated_data(UserSearchRequestSerializer, request.query_params)
        input_data = search_use_case.Input(**validated_data)
        output = search_use_case.execute(input_data)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def filter(self, request, filter_use_case: FilterUseCase = Provide[container.users.filter_use_case]):
        validated_data = self._validated_data(UserFilterRequestSerializer, request.query_params)
        input_data = filter_use_case.Input(**validated_data)
        output = filter_use_case.execute(input_data)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def find_by_id(self, request, find_by_id_use_case: FindByIdUseCase = Provide[container.users.find_by_id_use_case]):
        validated_data = self._validated_data(UserIdSerializer, request.query_params)
        input_data = find_by_id_use_case.Input(**validated_data)
        output = find_by_id_use_case.execute(input_data)
        data = self._to_response(UserResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def find_by_ids(self, request, find_by_ids_use_case: FindByIdsUseCase = Provide[container.users.find_by_ids_use_case]):
        validated_data = self._validated_data(UserIdSerializer, request.query_params, many=True)
        input_data = find_by_ids_use_case.Input(**validated_data)
        output = find_by_ids_use_case.execute(input_data)
        data = self._to_response(UserResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def exists_by_id(self, request, exists_by_id_use_case: ExistsByIdUseCase = Provide[container.users.exists_by_id_use_case]):
        validated_data = self._validated_data(UserIdSerializer, request.query_params)
        input_data = exists_by_id_use_case.Input(**validated_data)
        output = exists_by_id_use_case.execute(input_data)
        data = self._to_response(UserExistsResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def exists_by_ids(self, request, exists_by_ids_use_case: ExistsByIdsUseCase = Provide[container.users.exists_by_ids_use_case]):
        validated_data = self._validated_data(UserIdSerializer, request.query_params, many=True)
        input_data = exists_by_ids_use_case.Input(**validated_data)
        output = exists_by_ids_use_case.execute(input_data)
        data = self._to_response(UserExistsResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def _run_use_case(use_case, input_serializer, output_serializer, source, status_code=status.HTTP_200_OK, **kwargs):
        validated = UserViewSet._validated_data(input_serializer, source, **kwargs)
        input_data = use_case.Input(**validated)
        output = use_case.execute(input_data)
        data = UserViewSet._to_response(output_serializer, output, **kwargs)
        return Response(data, status=status_code)
    
    @staticmethod
    def _validated_data(serializer_class: Type[Serializer], data: dict[str, Any] | List[dict[str, Any]] | Any, **kwargs) -> Any:
        serializer = serializer_class(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _to_response(serializer_class: Type[Serializer], output: Union[dict, List[dict], Any], **kwargs) -> Union[dict, List[dict], Any]:
        serializer = serializer_class(output, **kwargs)
        return serializer.data