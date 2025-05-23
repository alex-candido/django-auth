# django_app/modules/v1/users/seedwork/use_cases.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')

class UseCases(ABC, Generic[Input, Output]):

    @abstractmethod
    def execute(self, input_param: Input) -> Output:
        raise NotImplementedError()
