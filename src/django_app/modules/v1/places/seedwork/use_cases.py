# django_app/modules/v1/places/seedwork/use_cases.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')

class UseCases(Generic[Input, Output], ABC):
    @abstractmethod
    def execute(self, input_param: Input) -> Output:
        pass