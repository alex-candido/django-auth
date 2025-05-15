from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Params = TypeVar('Params')
Output = TypeVar('Output')

class Repositories(ABC, Generic[Params]):
    
    @abstractmethod
    def find_one(self, params: Params) -> Output:
        raise NotImplementedError()
