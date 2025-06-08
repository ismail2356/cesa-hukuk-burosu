#!/usr/bin/env python
# Bu dosya yönetim komutu olarak değil, doğrudan çalıştırılabilir komut dosyası olarak kullanılacak

import os
import django
import sys

# Django ayarlarını yükle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CESA_Hukuk_Burosu.settings')
django.setup()

from django.contrib.auth.models import User

def main():
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@cesahukuk.com')
    password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
    
    if not User.objects.filter(username=username).exists():
        print('Süper kullanıcı oluşturuluyor...')
        User.objects.create_superuser(username, email, password)
        print('Süper kullanıcı başarıyla oluşturuldu!')
    else:
        print('Süper kullanıcı zaten mevcut!')

if __name__ == '__main__':
    main() 