import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Otomatik olarak süper kullanıcı oluşturur'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@cesahukuk.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
        
        if not User.objects.filter(username=username).exists():
            self.stdout.write('Süper kullanıcı oluşturuluyor...')
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Süper kullanıcı başarıyla oluşturuldu!'))
        else:
            self.stdout.write(self.style.WARNING('Süper kullanıcı zaten mevcut!')) 