# django_app/modules/v1/places/use_cases.py

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from rest_framework.exceptions import NotFound

from .seedwork.dto import ListInput, ListOutput

from .models import Place
from .repositories import PlaceRepository
from .seedwork.use_cases import UseCases

@dataclass(slots=True, frozen=True)
class FindOneUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: Optional[int] = None
        uuid: Optional[str] = None
        slug: Optional[str] = None
        name: Optional[str] = None

    @dataclass(slots=True, frozen=True)
    class Output:
        place: Optional[Place]

    def execute(self, input_param: 'Input') -> 'Output':
        place = self.repository.find_one(params=input_param)
        if place is None:
            raise NotFound(detail="Place not found.")
        return self.Output(place=place)

@dataclass(slots=True, frozen=True)
class FindAllUseCase(UseCases):
    repository: PlaceRepository

    class Input(ListInput[dict]):
        pass

    class Output(ListOutput[Place]):
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
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        slug: Optional[str] = None
        description: Optional[str] = None
        address: Optional[str] = None
        city: Optional[str] = None
        state: Optional[str] = None
        country: Optional[str] = None
        postal_code: Optional[str] = None
        website: Optional[str] = None
        phone: Optional[str] = None
        email: Optional[str] = None
        type: int = 0
        status: int = 0
        latitude: Optional[float] = None
        longitude: Optional[float] = None

    @dataclass(slots=True, frozen=True)
    class Output:
        place: Place

    def execute(self, input_param: 'Input') -> 'Output':
        data = asdict(input_param)
        place = self.repository.create_one(data=data)
        return self.Output(place=place)

@dataclass(slots=True, frozen=True)
class CreateManyUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        places: List[dict]

    @dataclass(slots=True, frozen=True)
    class Output:
        places: List[Place]

    def execute(self, input_param: 'Input') -> 'Output':
        places = self.repository.create_many(data_list=input_param.places)
        return self.Output(places=places)

@dataclass(slots=True, frozen=True)
class UpdateOneUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int
        name: Optional[str] = None
        slug: Optional[str] = None
        description: Optional[str] = None
        address: Optional[str] = None
        city: Optional[str] = None
        state: Optional[str] = None
        country: Optional[str] = None
        postal_code: Optional[str] = None
        website: Optional[str] = None
        phone: Optional[str] = None
        email: Optional[str] = None
        type: Optional[int] = None
        status: Optional[int] = None
        latitude: Optional[float] = None
        longitude: Optional[float] = None

    @dataclass(slots=True, frozen=True)
    class Output:
        place: Place

    def execute(self, input_param: 'Input') -> 'Output':
        data = {k: v for k, v in asdict(input_param).items() if k != 'id' and v is not None}
        place = self.repository.update_one(place_id=input_param.id, data=data)
        if place is None:
            raise NotFound(detail="Place not found.")
        return self.Output(place=place)

@dataclass(slots=True, frozen=True)
class UpdateManyUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        places: List[dict]

    @dataclass(slots=True, frozen=True)
    class Output:
        places: List[Place]

    def execute(self, input_param: 'Input') -> 'Output':
        places = self.repository.update_many(places_data=input_param.places)
        return self.Output(places=places)

@dataclass(slots=True, frozen=True)
class RemoveOneUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int

    def execute(self, input_param: 'Input') -> None:
        result = self.repository.remove_one(place_id=input_param.id)
        if not result:
            raise NotFound(detail="Place not found.")

@dataclass(slots=True, frozen=True)
class RemoveManyUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        ids: List[int]

    def execute(self, input_param: 'Input') -> None:
        self.repository.remove_many(place_ids=input_param.ids)

@dataclass(slots=True, frozen=True)
class SearchUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input(ListInput[dict]):
        query: str
        field: str

    class Output(ListOutput[Place]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        list_data = self.repository.search(
            query=input_param.query,
            field=input_param.field,
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir
        )
        return self.Output(**list_data)

@dataclass(slots=True, frozen=True)
class FilterUseCase(UseCases):
    repository: PlaceRepository

    class Input(ListInput[dict]):
        pass

    class Output(ListOutput[Place]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        list_data = self.repository.filter(
            filters=input_param.filter,
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir
        )
        return self.Output(**list_data)

@dataclass(slots=True, frozen=True)
class FindByIdUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int

    @dataclass(slots=True, frozen=True)
    class Output:
        place: Place

    def execute(self, input_param: 'Input') -> 'Output':
        place = self.repository.find_by_id(place_id=input_param.id)
        if place is None:
            raise NotFound(detail="Place not found.")
        return self.Output(place=place)

@dataclass(slots=True, frozen=True)
class FindByIdsUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        ids: List[int]

    @dataclass(slots=True, frozen=True)
    class Output:
        places: List[Place]

    def execute(self, input_param: 'Input') -> 'Output':
        places = self.repository.find_by_ids(place_ids=input_param.ids)
        return self.Output(places=places)

@dataclass(slots=True, frozen=True)
class ExistsByIdUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: int

    @dataclass(slots=True, frozen=True)
    class Output:
        id: int
        exists: bool

    def execute(self, input_param: 'Input') -> 'Output':
        exists = self.repository.exists_by_id(place_id=input_param.id)
        return self.Output(id=input_param.id, exists=exists)

@dataclass(slots=True, frozen=True)
class ExistsByIdsUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        ids: List[int]

    @dataclass(slots=True, frozen=True)
    class Output:
        results: List[Dict[str, Any]]

    def execute(self, input_param: 'Input') -> 'Output':
        results = self.repository.exists_by_ids(place_ids=input_param.ids)
        return self.Output(results=results)

# Geo-specific use cases

@dataclass(slots=True, frozen=True)
class NearbyPlacesUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input(ListInput[dict]):
        latitude: float
        longitude: float
        radius: float = 5000  # Default 5km radius

    class Output(ListOutput[Place]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        list_data = self.repository.g_near(
            latitude=input_param.latitude,
            longitude=input_param.longitude,
            radius=input_param.radius,
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir
        )
        return self.Output(**list_data)

@dataclass(slots=True, frozen=True)
class WithinBoxUseCase(UseCases):
    repository: PlaceRepository

    @dataclass(slots=True, frozen=True)
    class Input(ListInput[dict]):
        min_lat: float
        min_lng: float
        max_lat: float
        max_lng: float

    class Output(ListOutput[Place]):
        pass

    def execute(self, input_param: 'Input') -> 'Output':
        list_data = self.repository.g_within_box(
            min_lat=input_param.min_lat,
            min_lng=input_param.min_lng,
            max_lat=input_param.max_lat,
            max_lng=input_param.max_lng,
            page=input_param.page,
            per_page=input_param.per_page,
            sort=input_param.sort,
            sort_dir=input_param.sort_dir
        )
        return self.Output(**list_data)