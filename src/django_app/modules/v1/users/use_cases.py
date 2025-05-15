# django_app/modules/v1/users/use_cases.py

from dataclasses import dataclass
from typing import Optional
from rest_framework.exceptions import NotFound

from .models import User
from .repositories import UserRepository
from .seedwork.use_cases import UseCases

@dataclass(slots=True, frozen=True)
class FindOneUseCase(UseCases):
    
    repository: UserRepository

    @dataclass(slots=True, frozen=True)
    class Input:
        id: Optional[str] = None
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
