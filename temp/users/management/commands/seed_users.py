# from django.core.management.base import BaseCommand
# from django.db import transaction
# from django_app.modules.v1.users.repositories import UserRepository
# from faker import Faker
# import random
# from allauth.account.models import EmailAddress

# class Command(BaseCommand):
#     help = 'Seeds the database with initial user data'

#     def add_arguments(self, parser):
#         parser.add_argument(
#             '--mode',
#             type=str,
#             default='development',
#             help='Seeding mode: development or production',
#         )
#         parser.add_argument(
#             '--count',
#             type=int,
#             default=10,
#             help='Number of users to create (only in development mode)',
#         )

#     def _generate_random_password(self, length=12):
#         chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
#         return ''.join(random.choice(chars) for _ in range(length))

#     def _create_admin_user(self):
#         return {
#             'username': 'admin',
#             'email': 'admin@example.com',
#             'password': 'Admin@123',
#             'first_name': 'Admin',
#             'last_name': 'User',
#             'is_staff': True,
#             'is_superuser': True,
#         }

#     def _create_test_user(self):
#         return {
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'password': 'Test@123',
#             'first_name': 'Test',
#             'last_name': 'User',
#             'is_staff': False,
#             'is_superuser': False,
#         }

#     def _create_fake_user(self, fake):
#         return {
#             'username': fake.user_name(),
#             'email': fake.email(),
#             # 'password': self._generate_random_password(),
#             'password': 'User@123',
#             'first_name': fake.first_name(),
#             'last_name': fake.last_name(),
#             'is_staff': False,
#             'is_superuser': False,
#         }

#     def _seed_development(self, count):
#         user_repo = UserRepository()
#         fake = Faker()

#         users_data = [
#             self._create_admin_user(),
#             self._create_test_user(),
#         ] + [self._create_fake_user(fake) for _ in range(count)]

#         usernames = [user['username'] for user in users_data]
#         existing_users = set(
#             user_repo.find_all().filter(username__in=usernames).values_list('username', flat=True)
#         )

#         users_to_create = [user for user in users_data if user['username'] not in existing_users]

#         if users_to_create:
#             with transaction.atomic():
#                 created_users = user_repo.create_many(users_to_create)
#                 for user in created_users:
#                     self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))

#                     # Aqui adiciona o e-mail na tabela de emailaddress e marca como verificado
#                     EmailAddress.objects.create(
#                         user=user,
#                         email=user.email,
#                         verified=True,
#                         primary=True,
#                     )
#         else:
#             self.stdout.write(self.style.WARNING("No new users to create. All already exist."))

#     def _seed_production(self):
#         user_repo = UserRepository()
#         admin_data = self._create_admin_user()

#         if not user_repo.find_one({'username': admin_data['username']}):
#             user_repo.create_one(admin_data)
#             self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin_data['username']}"))
#         else:
#             self.stdout.write(self.style.WARNING(f"Admin user already exists: {admin_data['username']}"))

#     def handle(self, *args, **options):
#         mode = options['mode']
#         count = options['count']

#         self.stdout.write(self.style.SUCCESS(f"Starting user seeding in {mode} mode"))

#         if mode == 'development':
#             self._seed_development(count)
#         elif mode == 'production':
#             self._seed_production()
#         else:
#             self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}"))

#         self.stdout.write(self.style.SUCCESS("User seeding completed"))
