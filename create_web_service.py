import requests
import json
import uuid

# Render API bilgileri
API_KEY = "rnd_uzQg8XKYy9umEbnYgSlQcU6dq9DL"  # Yeni API anahtarı
API_URL = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Veritabanı bilgileri (check_db.py'den aldık)
DB_ID = "dpg-d12nacumcj7s73fhvq2g-a"
DB_NAME = "cesa_db"
DB_USER = "cesa_db_user"
OWNER_ID = "tea-d12muq3uibrs73fcuimg"

def create_web_service():
    print("Web servisi oluşturuluyor...")
    
    # İç ağ veritabanı bağlantı dizesi
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    print(f"Veritabanı bağlantı dizesi: {db_connection_string}")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    
    # Web servisi verilerini hazırla
    service_data = {
        "name": "cesa-hukuk",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "serviceDetails": {
            "runtime": "python",
            "buildCommand": "./build.sh",
            "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
            "plan": "starter",
            "env": "python",
            "numInstances": 1,
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
    }
    
    # API'ye isteği gönder
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
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
        return None

if __name__ == "__main__":
    create_web_service() 