from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser automatically from environment variables'

    def handle(self, *args, **options):
        username = settings('DJANGO_SUPERUSER_USERNAME')
        email = settings('DJANGO_SUPERUSER_EMAIL')
        password = settings('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR('Environment variables for superuser not properly set.'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))
