# django_app/modules/v1/places/container.py

from dependency_injector import containers, providers
from .repositories import PlaceRepository
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

class PlaceContainer(containers.DeclarativeContainer):
    place_repository = providers.Singleton(PlaceRepository)

    find_one_use_case = providers.Factory(FindOneUseCase, repository=place_repository)
    find_all_use_case = providers.Factory(FindAllUseCase, repository=place_repository)
    create_one_use_case = providers.Factory(CreateOneUseCase, repository=place_repository)
    create_many_use_case = providers.Factory(CreateManyUseCase, repository=place_repository)
    update_one_use_case = providers.Factory(UpdateOneUseCase, repository=place_repository)
    update_many_use_case = providers.Factory(UpdateManyUseCase, repository=place_repository)
    remove_one_use_case = providers.Factory(RemoveOneUseCase, repository=place_repository)
    remove_many_use_case = providers.Factory(RemoveManyUseCase, repository=place_repository)
    search_use_case = providers.Factory(SearchUseCase, repository=place_repository)
    filter_use_case = providers.Factory(FilterUseCase, repository=place_repository)
    find_by_id_use_case = providers.Factory(FindByIdUseCase, repository=place_repository)
    find_by_ids_use_case = providers.Factory(FindByIdsUseCase, repository=place_repository)
    exists_by_id_use_case = providers.Factory(ExistsByIdUseCase, repository=place_repository)
    exists_by_ids_use_case = providers.Factory(ExistsByIdsUseCase, repository=place_repository)
    
    # Geo-specific use cases
    nearby_places_use_case = providers.Factory(NearbyPlacesUseCase, repository=place_repository)
    within_box_use_case = providers.Factory(WithinBoxUseCase, repository=place_repository)