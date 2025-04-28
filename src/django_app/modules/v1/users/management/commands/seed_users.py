# django_app/modules/v1/users/management/commands/seed_users.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django_app.modules.v1.users.repositories import UserRepository
import random
import string


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
            help='Number of regular users to create (development mode only)',
        )

    def _generate_password(self, length=12):
        """Generate a random secure password"""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    def _create_admin_user(self):
        """Create an admin user"""
        admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'Admin@123',  # In production, use environment variables
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
        return admin_data

    def _create_test_user(self):
        """Create a test user"""
        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test@123',  # In production, use environment variables
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False,
        }
        return test_data

    def _create_random_user(self, index):
        """Create a random user for development purposes"""
        username = f'user{index}'
        user_data = {
            'username': username,
            'email': f'{username}@example.com',
            'password': f'User{index}@123',  # In production, use generated passwords
            'first_name': f'User{index}',
            'last_name': 'Sample',
            'is_staff': False,
            'is_superuser': False,
        }
        return user_data

    def _seed_development(self, count):
        """Seed database with development data"""
        user_repo = UserRepository()
        users_data = []

        # Add admin user
        users_data.append(self._create_admin_user())

        # Add test user
        users_data.append(self._create_test_user())

        # Add random users
        for i in range(1, count + 1):
            users_data.append(self._create_random_user(i))

        # Create users in bulk
        with transaction.atomic():
            for user_data in users_data:
                try:
                    # Check if user already exists
                    if not user_repo.find_one({'username': user_data['username']}):
                        user_repo.create_one(user_data)
                        self.stdout.write(self.style.SUCCESS(f"Created user: {user_data['username']}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"User already exists: {user_data['username']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating user {user_data['username']}: {str(e)}"))

    def _seed_production(self):
        """Seed database with production data"""
        user_repo = UserRepository()

        # In production, we typically only create an admin user if it doesn't exist
        admin_data = self._create_admin_user()
        
        try:
            # Check if admin already exists
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