# django_app/modules/v1/places/seedwork/dto.py

from dataclasses import dataclass, field
from typing import Generic, List, TypeVar, Dict, Any, Optional

T = TypeVar('T')

@dataclass
class ListInput(Generic[T]):
    page: int = 1
    per_page: int = 10
    sort: str = 'id'
    sort_dir: str = 'asc'
    filter: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ListOutput(Generic[T]):
    items: List[T]
    total: int
    current_page: int
    per_page: int
    last_page: int