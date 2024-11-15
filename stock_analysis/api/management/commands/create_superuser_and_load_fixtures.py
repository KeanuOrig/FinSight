from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist and loads fixtures.'

    def handle(self, *args, **kwargs):
        # Check if the superuser exists
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

        if not User.objects.filter(username=username).exists():
            # Create the superuser
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))

        # Load the fixtures (you can specify the fixture file if needed)
        try:
            # Replace 'your_fixture.json' with your actual fixture file(s)
            call_command('loaddata', 'stock_analysis/stocks/fixtures/blue_chip_stocks.json')
            self.stdout.write(self.style.SUCCESS('Fixtures loaded successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading fixtures: {e}'))
