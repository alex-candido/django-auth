# django_app/modules/v1/users/management/commands/seed_users.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django_app.modules.v1.users.repositories import UserRepository
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Seeds the database with initial user data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of users to create (only in development mode)',
        )

    def _generate_random_password(self, length=12):
        """Generate a random password"""
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        return ''.join(random.choice(chars) for _ in range(length))

    def _create_admin_user(self):
        """Create an admin user"""
        return {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'Admin@123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }

    def _create_test_user(self):
        """Create a test user"""
        return {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test@123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False,
        }

    def _create_fake_user(self, fake):
        """Generate fake user data"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = fake.user_name()
        email = fake.email()
        password = self._generate_random_password()

        return {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': False,
            'is_superuser': False,
        }

    def _seed_development(self, count):
        """Seed development database"""
        user_repo = UserRepository()
        fake = Faker()
        users_data = []

        # Add admin and test users
        users_data.append(self._create_admin_user())
        users_data.append(self._create_test_user())

        # Add fake users
        for _ in range(count):
            users_data.append(self._create_fake_user(fake))

        with transaction.atomic():
            for user_data in users_data:
                try:
                    if not user_repo.find_one({'username': user_data['username']}):
                        user_repo.create_one(user_data)
                        self.stdout.write(self.style.SUCCESS(f"Created user: {user_data['username']}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"User already exists: {user_data['username']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating user {user_data['username']}: {str(e)}"))

    def _seed_production(self):
        """Seed production database"""
        user_repo = UserRepository()
        admin_data = self._create_admin_user()

        try:
            if not user_repo.find_one({'username': admin_data['username']}):
                user_repo.create_one(admin_data)
                self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin_data['username']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Admin user already exists: {admin_data['username']}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating admin user: {str(e)}"))

    def handle(self, *args, **options):
        mode = options['mode']
        count = options['count']

        self.stdout.write(self.style.SUCCESS(f"Starting user seeding in {mode} mode"))

        if mode == 'development':
            self._seed_development(count)
        elif mode == 'production':
            self._seed_production()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}"))

        self.stdout.write(self.style.SUCCESS("User seeding completed"))
