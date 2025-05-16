# django_app/modules/v1/users/seedwork/repositories.py

from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar, Any

Params = TypeVar('Params')
Output = TypeVar('Output')

class Repositories(ABC, Generic[Params, Output]):

    @abstractmethod
    def find_one(self, params: Params) -> Output:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self, page: Optional[int] = None, per_page: Optional[int] = None, sort: Optional[str] = None, sort_dir: Optional[str] = None, filters: Optional[dict] = None) -> Dict:
        raise NotImplementedError()

    @abstractmethod
    def create_one(self, *args: Any, **kwargs: Any) -> Output:
        raise NotImplementedError()

    @abstractmethod
    def create_many(self, *args: Any, **kwargs: Any) -> List[Output]:
        raise NotImplementedError()

    @abstractmethod
    def update_one(self, *args: Any, **kwargs: Any) -> Optional[Output]:
        raise NotImplementedError()

    @abstractmethod
    def update_many(self, *args: Any, **kwargs: Any) -> List[Output]:
        raise NotImplementedError()

    @abstractmethod
    def remove_one(self, id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def remove_many(self, ids: List[int]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def search(self, query: str, field: str, page: Optional[int] = None, per_page: Optional[int] = None, sort: Optional[str] = None, sort_dir: Optional[str] = None, filters: Optional[dict] = None) -> Dict:
        raise NotImplementedError()

    @abstractmethod
    def filter(self, page: Optional[int] = None, per_page: Optional[int] = None, sort: Optional[str] = None, sort_dir: Optional[str] = None, filters: Optional[dict] = None) -> Dict:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Output]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_ids(self, ids: List[int]) -> List[Output]:
        raise NotImplementedError()

    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def exists_by_ids(self, ids: List[int]) -> Dict[int, bool]:
        raise NotImplementedError()