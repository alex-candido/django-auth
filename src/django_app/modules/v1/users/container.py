# django_app/modules/v1/users/container.py

from dependency_injector import containers, providers
from .repositories import UserRepository
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

class UserContainer(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserRepository)

    find_one_use_case = providers.Factory(FindOneUseCase, repository=user_repository)
    find_all_use_case = providers.Factory(FindAllUseCase, repository=user_repository)
    create_one_use_case = providers.Factory(CreateOneUseCase, repository=user_repository)
    create_many_use_case = providers.Factory(CreateManyUseCase, repository=user_repository)
    update_one_use_case = providers.Factory(UpdateOneUseCase, repository=user_repository)
    update_many_use_case = providers.Factory(UpdateManyUseCase, repository=user_repository)
    remove_one_use_case = providers.Factory(RemoveOneUseCase, repository=user_repository)
    remove_many_use_case = providers.Factory(RemoveManyUseCase, repository=user_repository)
    search_use_case = providers.Factory(SearchUseCase, repository=user_repository)
    filter_use_case = providers.Factory(FilterUseCase, repository=user_repository)
    find_by_id_use_case = providers.Factory(FindByIdUseCase, repository=user_repository)
    find_by_ids_use_case = providers.Factory(FindByIdsUseCase, repository=user_repository)
    exists_by_id_use_case = providers.Factory(ExistsByIdUseCase, repository=user_repository)
    exists_by_ids_use_case = providers.Factory(ExistsByIdsUseCase, repository=user_repository)