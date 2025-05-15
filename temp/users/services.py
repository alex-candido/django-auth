# django_app/modules/v1/users/services.py

from .repositories import UserRepository

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def find_one(self, params):
        user = self.repository.find_one(params)
        return user

    def find_all(self):
        users = self.repository.find_all()
        return users

    def create_one(self, data):
        user = self.repository.create_one(data)
        return user

    def create_many(self, data_list):
        users = self.repository.create_many(data_list)
        return users

    def update_one(self, data):
        user = self.repository.update_one(data)
        return user

    def update_many(self, data_list):
        users = self.repository.update_many(data_list)
        return users

    def remove_one(self, params):
        return self.repository.remove_one(params)

    def remove_many(self, params):
        return self.repository.remove_many(params)

    def search(self, data):
        users = self.repository.search(data)
        return users

    def filter(self, data):
        users = self.repository.filter(data)
        return users

    def find_by_id(self, id):
        user = self.repository.find_by_id(id)
        return user

    def find_by_ids(self, ids):
        users = self.repository.find_by_ids(ids)
        return users

    def exists_by_id(self, id):
        return self.repository.exists_by_id(id)

    def exists_by_ids(self, ids):
        return self.repository.exists_by_ids(ids)
