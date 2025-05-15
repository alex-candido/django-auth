# django_app/modules/v1/users/repositories.py

from dataclasses import asdict
from typing import Optional
from .models import User

from .seedwork.repositories import Repositories
from .use_cases import FindOneUseCase

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class UserRepository(Repositories):
    def find_one(self, params: FindOneUseCase.Input) -> Optional[User]:
        try:
            filters = asdict(params) 
            return User.objects.get(**filters)
        except User.DoesNotExist:
            return None

  