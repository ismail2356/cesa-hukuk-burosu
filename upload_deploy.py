import requests
import json
import uuid
import os

# Render API bilgileri
API_KEY = "rnd_uzQg8XKYy9umEbnYgSlQcU6dq9DL"
API_URL = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# Veritabanı bilgileri
DB_ID = "dpg-d12nacumcj7s73fhvq2g-a"
DB_NAME = "cesa_db"
DB_USER = "cesa_db_user"
OWNER_ID = "tea-d12muq3uibrs73fcuimg"

def upload_and_deploy():
    print("Dosya yüklemesi ile deploy işlemi başlatılıyor...")
    
    # İç ağ veritabanı bağlantı dizesi
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    print(f"Veritabanı bağlantı dizesi: {db_connection_string}")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    
    # ZIP dosyasını yükle
    zip_file_path = "cesa_hukuk_render.zip"
    if not os.path.exists(zip_file_path):
        print(f"Hata: {zip_file_path} dosyası bulunamadı!")
        return None
    
    print(f"ZIP dosyası yükleniyor: {zip_file_path}")
    
    # Dosya yükleme için multipart form data
    files = {
        'file': ('cesa_hukuk_render.zip', open(zip_file_path, 'rb'), 'application/zip')
    }
    
    # Web servisi oluşturma verisi
    service_data = {
        "name": "cesa-hukuk",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "buildCommand": "./build.sh",
        "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
        "plan": "starter",
        "runtime": "python",
        "envVars": [
            {
                "key": "DATABASE_URL",
                "value": db_connection_string
            },
            {
                "key": "SECRET_KEY",
                "value": secret_key
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
                "value": "Admin123!"
            },
            {
                "key": "PORT",
                "value": "10000"
            }
        ]
    }
    
    # Multipart formdata ile gönder
    data = {
        'serviceData': json.dumps(service_data)
    }
    
    # Dosya yüklemeli POST isteği
    response = requests.post(
        f"{API_URL}/services/upload",
        headers={"Authorization": f"Bearer {API_KEY}"},
        files=files,
        data=data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        service_info = response.json()
        print("Web servisi başarıyla oluşturuldu!")
        print(json.dumps(service_info, indent=2))
        return service_info
    else:
        print(f"Web servisi oluşturma hatası:")
        print(f"Response: {response.text}")
        
        # Alternatif endpoint deneyelim
        print("\nAlternatif endpoint deneniyor...")
        try_alternative_upload(files, service_data)
        
        return None

def try_alternative_upload(files, service_data):
    # Alternatif endpoint: /uploads veya /deploy
    alternative_endpoints = [
        f"{API_URL}/uploads",
        f"{API_URL}/deploy",
        f"{API_URL}/services/deploy"
    ]
    
    for endpoint in alternative_endpoints:
        print(f"Deneniyor: {endpoint}")
        
        response = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files=files,
            data={'serviceData': json.dumps(service_data)}
        )
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}...")
        
        if response.status_code == 201:
            print("Başarılı!")
            return response.json()

if __name__ == "__main__":
    upload_and_deploy() 