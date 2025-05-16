# django_app/modules/v1/users/repositories.py

from dataclasses import asdict
from typing import Optional, List, Dict, Any

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet

from .filters import UserFilter
from .models import User
from .seedwork.repositories import Repositories

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class UserRepository(Repositories):
    def find_one(self, params) -> Optional[User]:
        filters = {k: v for k, v in asdict(params).items() if v is not None}
        try:
            return User.objects.get(**filters)
        except User.DoesNotExist: # pylint: disable=no-member
            return None

    def find_all(self, page: Optional[int] = None, per_page: Optional[int] = None, sort: Optional[str] = None, sort_dir: Optional[str] = None, filters: Optional[dict] = None) -> Dict:
        queryset = User.objects.all()
        ordering = UserRepository._build_ordering(sort, sort_dir)
        if ordering:
            queryset = queryset.order_by(ordering)
        return self._paginate_queryset(queryset, page, per_page)

    def create_one(self, username, email, password, first_name, last_name) -> User:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def create_many(self, users_data: List[dict]) -> List[User]:
        users = [User(**data) for data in users_data]
        return User.objects.bulk_create(users)

    def update_one(self, id: int, username: Optional[str] = None, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Optional[User]:
        try:
            user = User.objects.get(id=id)
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            user.save()
            return user
        except User.DoesNotExist: # pylint: disable=no-member
            return None

    def update_many(self, users_data: List[dict]) -> List[User]:
        updated_users = []
        for data in users_data:
            user_id = data.pop('id', None)
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    for key, value in data.items():
                        setattr(user, key, value)
                    updated_users.append(user)
                except User.DoesNotExist: # pylint: disable=no-member
                    pass # Handle as needed
        User.objects.bulk_update(updated_users, fields=['username', 'email', 'first_name', 'last_name'])
        return updated_users

    def remove_one(self, id: int) -> bool:
        try:
            user = User.objects.get(id=id)
            user.delete()
            return True
        except User.DoesNotExist: # pylint: disable=no-member
            return False

    def remove_many(self, ids: List[int]) -> None:
        User.objects.filter(id__in=ids).delete()

    def search(self, query: str, field: str, page: Optional[int] = None, per_page: Optional[int] = None, sort: Optional[str] = None, sort_dir: Optional[str] = None, filters: Optional[dict] = None) -> Dict:
        queryset = User.objects.filter(**{f'{field}__icontains': query})
        if filters:
            queryset = queryset.filter(**filters)
        ordering = UserRepository._build_ordering(sort, sort_dir)
        if ordering:
            queryset = queryset.order_by(ordering)
        return self._paginate_queryset(queryset, page, per_page)

    def filter(self, page: Optional[int] = None, per_page: Optional[int] = None, sort: Optional[str] = None, sort_dir: Optional[str] = None, filters: Optional[dict] = None) -> Dict:
        queryset = User.objects.all()
        user_filter = UserFilter(filters, queryset=queryset)
        queryset = user_filter.qs
        ordering = UserRepository._build_ordering(sort, sort_dir)
        if ordering:
            queryset = queryset.order_by(ordering)
        return self._paginate_queryset(queryset, page, per_page)

    def find_by_id(self, id: int) -> Optional[User]:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist: # pylint: disable=no-member
            return None

    def find_by_ids(self, ids: List[int]) -> List[User]:
        return list(User.objects.filter(id__in=ids))

    def exists_by_id(self, id: int) -> bool:
        return User.objects.filter(id=id).exists()

    def exists_by_ids(self, ids: List[int]) -> Dict[int, bool]:
        existing_ids = set(User.objects.filter(id__in=ids).values_list('id', flat=True))
        return {user_id: user_id in existing_ids for user_id in ids}

    def _paginate_queryset(self, queryset: QuerySet, page: Optional[int] = None, per_page: Optional[int] = None) -> Dict:
        if per_page:
            paginator = Paginator(queryset, per_page)
            try:
                page_number = page if page is not None else 1
                users_page = paginator.page(page_number)
            except PageNotAnInteger:
                users_page = paginator.page(1)
            except EmptyPage:
                users_page = paginator.page(paginator.num_pages)
            return UserRepository._build_pagination_response(users_page, paginator)
        else:
            return UserRepository._build_pagination_response(queryset, None)

    @staticmethod
    def _build_pagination_response(users_page: Any, paginator: Optional[Paginator]) -> Dict:
        if paginator:
            return {
                'items': list(users_page.object_list),
                'total': paginator.count,
                'current_page': users_page.number,
                'per_page': paginator.per_page,
                'last_page': paginator.num_pages
            }
        else:
            return {
                'items': list(users_page),
                'total': len(users_page),
                'current_page': 1,
                'per_page': len(users_page) if len(users_page) > 0 else 1,
                'last_page': 1
            }

    @staticmethod
    def _build_ordering(sort_field: Optional[str], sort_direction: Optional[str]) -> Optional[str]:
        if sort_field:
            return sort_field if sort_direction == 'asc' else f'-{sort_field}'
        return None