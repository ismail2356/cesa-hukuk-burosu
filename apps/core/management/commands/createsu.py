from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Otomatik olarak superuser oluşturur'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@cesahukuk.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin')

        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Superuser oluşturuluyor: {username}'))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser başarıyla oluşturuldu'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser zaten mevcut: {username}')) 