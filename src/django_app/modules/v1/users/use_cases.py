# django_app/modules/v1/users/use_cases.py

from dataclasses import dataclass, asdict
from typing import Optional, List
from rest_framework.exceptions import NotFound

from .seedwork.dto import ListInput, ListOutput

from .models import User
from .repositories import UserRepository
from .seedwork.use_cases import UseCases

@dataclass(slots=True, frozen=True)
class FindOneUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        id: Optional[int] = None
        uuid: Optional[str] = None
        username: Optional[str] = None
        email: Optional[str] = None

    @dataclass(slots=True, frozen=True)
    class Output:
        user: Optional[User]

    def execute(self, input_param: 'Input') -> 'Output':
        user = self.repository.find_one(params=input_param)
        if user is None:
            raise NotFound(detail="User not found.")
        return self.Output(user=user)

@dataclass(slots=True, frozen=True)
class FindAllUseCase(UseCases):
    repository: 'UserRepository'

    class Input(ListInput[dict]):
        pass

    class Output(ListOutput[User]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        list_data = self.repository.find_all(
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir,
            filters=input_param.filter
        )
        return self.Output(**list_data)

@dataclass(slots=True, frozen=True)
class CreateOneUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        username: str
        email: str
        password: str
        first_name: str
        last_name: str

    @dataclass(slots=True, frozen=True)
    class Output:
        user: User

    def execute(self, input_param: 'Input') -> 'Output':
        user = self.repository.create_one(
            username=input_param.username,
            email=input_param.email,
            password=input_param.password,
            first_name=input_param.first_name,
            last_name=input_param.last_name
        )
        return self.Output(user=user)

@dataclass(slots=True, frozen=True)
class CreateManyUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        users: List[dict]

    @dataclass(slots=True, frozen=True)
    class Output:
        users: List[User]

    def execute(self, input_param: 'Input') -> 'Output':
        users = self.repository.create_many(users_data=input_param.users)
        return self.Output(users=users)

@dataclass(slots=True, frozen=True)
class UpdateOneUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int
        username: Optional[str] = None
        email: Optional[str] = None
        first_name: Optional[str] = None
        last_name: Optional[str] = None

    @dataclass(slots=True, frozen=True)
    class Output:
        user: User

    def execute(self, input_param: 'Input') -> 'Output':
        user = self.repository.update_one(
            id=input_param.id,
            username=input_param.username,
            email=input_param.email,
            first_name=input_param.first_name,
            last_name=input_param.last_name
        )
        if user is None:
            raise NotFound(detail="User not found for update.")
        return self.Output(user=user)

@dataclass(slots=True, frozen=True)
class UpdateManyUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        users: List[dict]

    @dataclass(slots=True, frozen=True)
    class Output:
        users: List[User]

    def execute(self, input_param: 'Input') -> 'Output':
        users = self.repository.update_many(users_data=input_param.users)
        return self.Output(users=users)

@dataclass(slots=True, frozen=True)
class RemoveOneUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int

    class Output:
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        deleted = self.repository.remove_one(id=input_param.id)
        if not deleted:
            raise NotFound(detail="User not found for removal.")
        return self.Output()

@dataclass(slots=True, frozen=True)
class RemoveManyUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        ids: List[int]

    class Output:
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        self.repository.remove_many(ids=input_param.ids)
        return self.Output()

@dataclass(slots=True, frozen=True)
class SearchUseCase(UseCases):
    repository: 'UserRepository'

    class Input(ListInput[dict]):
        query: str
        field: str

    class Output(ListOutput[User]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        list_data = self.repository.search(
            query=input_param.query,
            field=input_param.field,
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir,
            filters=input_param.filter
        )
        return self.Output(**list_data)

@dataclass(slots=True, frozen=True)
class FilterUseCase(UseCases):
    repository: 'UserRepository'

    class Input(ListInput[dict]):
        uuid: Optional[str] = None
        username: Optional[str] = None
        email: Optional[str] = None
        first_name: Optional[str] = None
        last_name: Optional[str] = None

    class Output(ListOutput[User]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        filters = {k: v for k, v in asdict(input_param).items() if v is not None and k not in ['page', 'per_page', 'sort', 'sort_dir']}
        list_data = self.repository.filter(
            filters=filters,
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir
        )
        return self.Output(**list_data)

@dataclass(slots=True, frozen=True)
class FindByIdUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int

    @dataclass(slots=True, frozen=True)
    class Output:
        user: Optional[User]

    def execute(self, input_param: 'Input') -> 'Output':
        user = self.repository.find_by_id(id=input_param.id)
        if user is None:
            raise NotFound(detail="User not found.")
        return self.Output(user=user)

@dataclass(slots=True, frozen=True)
class FindByIdsUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        ids: List[int]

    @dataclass(slots=True, frozen=True)
    class Output:
        users: List[User]

    def execute(self, input_param: 'Input') -> 'Output':
        users = self.repository.find_by_ids(ids=input_param.ids)
        if not users:
            raise NotFound("No users found.")
        return self.Output(users=users)

@dataclass(slots=True, frozen=True)
class ExistsByIdUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int

    @dataclass(slots=True, frozen=True)
    class Output:
        id: int
        exists: bool

    def execute(self, input_param: 'Input') -> 'Output':
        exists = self.repository.exists_by_id(id=input_param.id)
        return self.Output(id=input_param.id, exists=exists)

@dataclass(slots=True, frozen=True)
class ExistsByIdsUseCase(UseCases):
    repository: 'UserRepository'

    @dataclass(slots=True, frozen=True)
    class Input:
        ids: List[int]

    @dataclass(slots=True, frozen=True)
    class Output:
        ids: List[int]
        exists: bool

    def execute(self, input_param: 'Input') -> 'Output':
        exists_map = self.repository.exists_by_ids(ids=input_param.ids)
        return self.Output(ids=list(exists_map.keys()), exists=all(exists_map.values()))