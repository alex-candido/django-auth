# django_app/modules/v1/places/api.py

from typing import List, Type, Union, Any
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from dependency_injector.wiring import inject, Provide
from .container import PlaceContainer
from .serializers import (
    PaginationRequestSerializer,
    PaginationResponseSerializer,
    PlaceCreateRequestSerializer,
    PlaceCreateResponseSerializer,
    PlaceExistsResponseSerializer,
    PlaceFilterRequestSerializer,
    PlaceResponseSerializer,
    PlaceSearchRequestSerializer,
    PlaceUpdateRequestSerializer,
    PlaceIdSerializer,
    PlaceSerializer,
    NearbyPlacesRequestSerializer,
    WithinBoxRequestSerializer,
    PlaceGeoFeatureSerializer
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
    NearbyPlacesUseCase,
    WithinBoxUseCase
)
from .repositories import PlaceRepository

class PlaceViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @inject
    def find_one(self, request, find_one_use_case: FindOneUseCase = Provide[PlaceContainer.find_one_use_case]):
        validated_data = self._validated_data(PlaceSerializer, request.query_params)
        input_param = find_one_use_case.Input(**validated_data)
        output = find_one_use_case.execute(input_param)
        data = self._to_response(PlaceResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @inject
    def find_all(self, request, find_all_use_case: FindAllUseCase = Provide[PlaceContainer.find_all_use_case]):
        validated_data = self._validated_data(PaginationRequestSerializer, request.query_params)
        input_param = find_all_use_case.Input(**validated_data)
        output = find_all_use_case.execute(input_param)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    @inject
    def create_one(self, request, create_one_use_case: CreateOneUseCase = Provide[PlaceContainer.create_one_use_case]):
        validated_data = self._validated_data(PlaceCreateRequestSerializer, request.data)
        input_data = create_one_use_case.Input(**validated_data)
        output = create_one_use_case.execute(input_data)
        data = self._to_response(PlaceCreateResponseSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    @inject
    def create_many(self, request, create_many_use_case: CreateManyUseCase = Provide[PlaceContainer.create_many_use_case]):
        validated_data = self._validated_data(PlaceCreateRequestSerializer, request.data, many=True)
        input_data = create_many_use_case.Input(places=validated_data)
        output = create_many_use_case.execute(input_data)
        data = self._to_response(PlaceCreateResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    @inject
    def update_one(self, request, update_one_use_case: UpdateOneUseCase = Provide[PlaceContainer.update_one_use_case]):
        validated_data = self._validated_data(PlaceUpdateRequestSerializer, request.data)
        input_data = update_one_use_case.Input(**validated_data)
        output = update_one_use_case.execute(input_data)
        data = self._to_response(PlaceResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    @inject
    def update_many(self, request, update_many_use_case: UpdateManyUseCase = Provide[PlaceContainer.update_many_use_case]):
        validated_data = self._validated_data(PlaceUpdateRequestSerializer, request.data, many=True)
        input_data = update_many_use_case.Input(places=validated_data)
        output = update_many_use_case.execute(input_data)
        data = self._to_response(PlaceResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    @inject
    def remove_one(self, request, remove_one_use_case: RemoveOneUseCase = Provide[PlaceContainer.remove_one_use_case]):
        validated_data = self._validated_data(PlaceIdSerializer, request.data)
        input_data = remove_one_use_case.Input(**validated_data)
        remove_one_use_case.execute(input_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    @inject
    def remove_many(self, request, remove_many_use_case: RemoveManyUseCase = Provide[PlaceContainer.remove_many_use_case]):
        validated_data = self._validated_data(PlaceIdSerializer, request.data, many=True)
        input_data = remove_many_use_case.Input(**validated_data)
        remove_many_use_case.execute(input_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def search(self, request, search_use_case: SearchUseCase = Provide[PlaceContainer.search_use_case]):
        validated_data = self._validated_data(PlaceSearchRequestSerializer, request.query_params)
        input_data = search_use_case.Input(**validated_data)
        output = search_use_case.execute(input_data)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def filter(self, request, filter_use_case: FilterUseCase = Provide[PlaceContainer.filter_use_case]):
        validated_data = self._validated_data(PlaceFilterRequestSerializer, request.query_params)
        input_data = filter_use_case.Input(**validated_data)
        output = filter_use_case.execute(input_data)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def find_by_id(self, request, find_by_id_use_case: FindByIdUseCase = Provide[PlaceContainer.find_by_id_use_case]):
        validated_data = self._validated_data(PlaceIdSerializer, request.query_params)
        input_data = find_by_id_use_case.Input(**validated_data)
        output = find_by_id_use_case.execute(input_data)
        data = self._to_response(PlaceResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def find_by_ids(self, request, find_by_ids_use_case: FindByIdsUseCase = Provide[PlaceContainer.find_by_ids_use_case]):
        validated_data = self._validated_data(PlaceIdSerializer, request.query_params, many=True)
        input_data = find_by_ids_use_case.Input(**validated_data)
        output = find_by_ids_use_case.execute(input_data)
        data = self._to_response(PlaceResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def exists_by_id(self, request, exists_by_id_use_case: ExistsByIdUseCase = Provide[PlaceContainer.exists_by_id_use_case]):
        validated_data = self._validated_data(PlaceIdSerializer, request.query_params)
        input_data = exists_by_id_use_case.Input(**validated_data)
        output = exists_by_id_use_case.execute(input_data)
        data = self._to_response(PlaceExistsResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def exists_by_ids(self, request, exists_by_ids_use_case: ExistsByIdsUseCase = Provide[PlaceContainer.exists_by_ids_use_case]):
        validated_data = self._validated_data(PlaceIdSerializer, request.query_params, many=True)
        input_data = exists_by_ids_use_case.Input(**validated_data)
        output = exists_by_ids_use_case.execute(input_data)
        data = self._to_response(PlaceExistsResponseSerializer, output, many=True)
        return Response(data, status=status.HTTP_200_OK)
    
    # Geo-specific actions
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def nearby(self, request, nearby_places_use_case: NearbyPlacesUseCase = Provide[PlaceContainer.nearby_places_use_case]):
        validated_data = self._validated_data(NearbyPlacesRequestSerializer, request.query_params)
        input_data = nearby_places_use_case.Input(**validated_data)
        output = nearby_places_use_case.execute(input_data)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    @inject
    def within_box(self, request, within_box_use_case: WithinBoxUseCase = Provide[PlaceContainer.within_box_use_case]):
        validated_data = self._validated_data(WithinBoxRequestSerializer, request.query_params)
        input_data = within_box_use_case.Input(**validated_data)
        output = within_box_use_case.execute(input_data)
        data = self._to_response(PaginationResponseSerializer, output)
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def _validated_data(serializer_class: Type[Serializer], data: dict[str, Any] | List[dict[str, Any]] | Any, **kwargs) -> Any:
        serializer = serializer_class(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _to_response(serializer_class: Type[Serializer], output: Union[dict, List[dict], Any], **kwargs) -> Union[dict, List[dict], Any]:
        serializer = serializer_class(output, **kwargs)
        return serializer.data
    
 