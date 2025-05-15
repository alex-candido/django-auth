from dataclasses import dataclass
from typing import Any

from .repositories import UsersRepository
from .seedwork.use_cases import UseCase

@dataclass(slots=True, frozen=True)
class FindOneUseCase(UseCase):
    repository: UsersRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str

    @dataclass(slots=True, frozen=True)
    class Output:
        user: Any 

    def execute(self, input_param: 'Input') -> 'Output':
        user = self.repository.find_one(input_param)
        return self.Output(user=user)
