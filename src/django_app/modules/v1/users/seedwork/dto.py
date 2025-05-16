# django_app/modules/v1/users/seedwork/dto.py

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

Filter = TypeVar('Filter')
Item = TypeVar('Item')

@dataclass(slots=True, frozen=True)
class ListOutput(Generic[Item]):
    items: List[Item]
    total: int
    current_page: int
    per_page: int
    last_page: int

@dataclass(slots=True, frozen=True)
class ListInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None