import os
import requests
import json
import time

# Render API bilgileri
API_KEY = os.environ.get('RENDER_API_KEY', 'rnd_iwBkK14XhwST3eQ3vGBtrq3BWU51')
API_URL = 'https://api.render.com/v1'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Render üzerinde PostgreSQL veritabanı oluşturma
def create_database():
    print("PostgreSQL veritabanı oluşturuluyor...")
    
    db_data = {
        "name": "cesa-db",
        "region": "frankfurt",  # Lokasyonu değiştirebilirsiniz
        "plan": "free",  # Ücretsiz plan
        "isPublic": False,
        "user": "cesa_user",
        "database": "cesa_hukuk"
    }
    
    response = requests.post(
        f'{API_URL}/postgres',  # Doğru endpoint
        headers=HEADERS,
        json=db_data
    )
    
    if response.status_code in [201, 200]:
        db_info = response.json()
        print(f"Veritabanı başarıyla oluşturuldu! ID: {db_info['id']}")
        return db_info
    else:
        print(f"Veritabanı oluşturma hatası: {response.status_code}")
        print(response.text)
        
        # Veritabanı zaten var mı kontrol edelim
        response = requests.get(f'{API_URL}/postgres', headers=HEADERS)
        if response.status_code == 200:
            databases = response.json()
            for db in databases:
                if db['name'] == 'cesa-db':
                    print(f"Veritabanı zaten mevcut! ID: {db['id']}")
                    return db
        
        return None

# Veritabanı bağlantı URL'sini alma
def get_database_connection_string(db_id):
    print("Veritabanı bağlantı bilgileri alınıyor...")
    
    response = requests.get(
        f'{API_URL}/postgres/{db_id}/connection-strings',  # Doğru connection strings endpoint
        headers=HEADERS
    )
    
    if response.status_code == 200:
        db_info = response.json()
        # Bağlantı dizesini internal_database_url'den alabiliriz
        connection_string = db_info.get('internalDatabaseUrl')
        if connection_string:
            print("Veritabanı bağlantı bilgileri başarıyla alındı.")
            return connection_string
        else:
            print("Bağlantı bilgileri bulunamadı.")
            return None
    else:
        print(f"Veritabanı bilgilerini alma hatası: {response.status_code}")
        print(response.text)
        return None

# Web service oluşturma
def create_web_service(db_connection_string):
    print("Web servisi oluşturuluyor...")
    
    service_data = {
        "name": "cesa-hukuk",
        "type": "web_service",
        "region": "frankfurt",  # Lokasyonu değiştirebilirsiniz
        "plan": "starter",      # Starter plan
        "runtime": "python",
        "buildCommand": "./build.sh",
        "startCommand": "python -m gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
        "envVars": [
            {
                "key": "DATABASE_URL",
                "value": db_connection_string
            },
            {
                "key": "SECRET_KEY",
                "value": "django-insecure-" + os.urandom(24).hex()
            },
            {
                "key": "DEBUG",
                "value": "false"
            },
            {
                "key": "ADMIN_USERNAME",
                "value": "admin"
            },
            {
                "key": "ADMIN_EMAIL",
                "value": "admin@cesahukuk.com"
            },
            {
                "key": "ADMIN_PASSWORD",
                "value": "admin123"  # Gerçek deploymentta güçlü bir parola kullanın!
            },
            {
                "key": "PYTHON_VERSION",
                "value": "3.11"
            }
        ],
        "autoDeploy": "yes"
    }
    
    response = requests.post(
        f'{API_URL}/services',
        headers=HEADERS,
        json=service_data
    )
    
    if response.status_code in [201, 200]:
        service_info = response.json()
        print(f"Web servisi başarıyla oluşturuldu! ID: {service_info['id']}")
        print(f"Deployment URL: {service_info.get('serviceDetails', {}).get('url')}")
        return service_info
    else:
        print(f"Web servisi oluşturma hatası: {response.status_code}")
        print(response.text)
        
        # Servis zaten var mı kontrol edelim
        response = requests.get(f'{API_URL}/services', headers=HEADERS)
        if response.status_code == 200:
            services = response.json()
            for service in services:
                if service['name'] == 'cesa-hukuk':
                    print(f"Web servisi zaten mevcut! ID: {service['id']}")
                    return service
        
        return None

# Ana fonksiyon
def deploy_to_render():
    print("CESA Hukuk Bürosu projesi Render'a deploy ediliyor...")
    
    # 1. Veritabanı oluştur
    db_info = create_database()
    if not db_info:
        print("Veritabanı oluşturulamadı. İşlem durduruldu.")
        return
    
    # 2. Veritabanı bağlantı bilgilerini al
    time.sleep(5)  # Veritabanının oluşturulması için biraz bekleyelim
    db_connection_string = get_database_connection_string(db_info['id'])
    if not db_connection_string:
        print("Veritabanı bağlantı bilgileri alınamadı. İşlem durduruldu.")
        return
    
    # 3. Web servisi oluştur
    service_info = create_web_service(db_connection_string)
    if not service_info:
        print("Web servisi oluşturulamadı. İşlem durduruldu.")
        return
    
    print("\n=== Deploy İşlemi Başarıyla Tamamlandı ===")
    print("Web sitenize Render URL'si üzerinden erişebilirsiniz.")
    print("Admin paneline giriş yapmak için:")
    print("Kullanıcı adı: admin")
    print("Şifre: admin123")
    print("\nÖzel alan adınızı bağlamak için Render dashboard'a gidin ve Custom Domain ekleyin.")

if __name__ == "__main__":
    deploy_to_render() 