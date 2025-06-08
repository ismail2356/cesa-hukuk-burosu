import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CESA_Hukuk_Burosu.settings')
django.setup()

# Admin kullanıcısı oluştur
from django.contrib.auth.models import User

# Eğer 'admin' kullanıcısı yoksa oluştur
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
    print("Admin kullanıcısı başarıyla oluşturuldu.")
else:
    print("Admin kullanıcısı zaten mevcut.") 