# django_app/modules/v1/users/repositories.py

from django.db.models import Q
from .models import User

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class UserRepository:
    def find_one(self, params):
        try:
            return User.objects.get(**params)
        except User.DoesNotExist:
            return None

    def find_all(self):
        return User.objects.all()

    def create_one(self, data):
        user = User.objects.create_user(**data)
        return user

    def create_many(self, data_list):
        users = [User.objects.create_user(**data) for data in data_list]
        return users

    def update_one(self, data):
        user = User.objects.get(id=data.pop('id'))
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user

    def update_many(self, data_list):
        users = []
        for data in data_list:
            user = User.objects.get(id=data.pop('id'))
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            users.append(user)
        return users

    def remove_one(self, params):
        user = User.objects.get(**params)
        user.delete()
        return {'id': params.get('id')}

    def remove_many(self, params):
        users = User.objects.filter(**params)
        ids = list(users.values_list('id', flat=True))
        users.delete()
        return {'ids': ids}

    def search(self, data):
        query = data.get('query')
        field = data.get('field')
        if field == 'username':
            return User.objects.filter(username__icontains=query)
        elif field == 'email':
            return User.objects.filter(email__icontains=query)
        elif field == 'first_name':
            return User.objects.filter(first_name__icontains=query)
        elif field == 'last_name':
            return User.objects.filter(last_name__icontains=query)
        return User.objects.none()

    def filter(self, data):
        query = Q()
        if data.get('role') == 'admin':
            query &= Q(is_staff=True)
        elif data.get('role') == 'user':
            query &= Q(is_staff=False)
        if data.get('status') == 'active':
            query &= Q(is_active=True)
        elif data.get('status') == 'inactive':
            query &= Q(is_active=False)
        return User.objects.filter(query)

    def find_by_id(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def find_by_ids(self, ids):
        return User.objects.filter(id__in=ids)

    def exists_by_id(self, id):
        return User.objects.filter(id=id).exists()

    def exists_by_ids(self, ids):
        existing_ids = User.objects.filter(id__in=ids).values_list('id', flat=True)
        return list(existing_ids)