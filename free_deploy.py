import requests
import json
import uuid

# Render API bilgileri
API_KEY = "rnd_uzQg8XKYy9umEbnYgSlQcU6dq9DL"
API_URL = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Veritabanı bilgileri
DB_ID = "dpg-d12nacumcj7s73fhvq2g-a"
DB_NAME = "cesa_db"
DB_USER = "cesa_db_user"
OWNER_ID = "tea-d12muq3uibrs73fcuimg"

def create_free_web_service():
    print("FREE plan ile web servisi oluşturuluyor...")
    
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    service_data = {
        "name": "cesa-hukuk-free",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "repo": "https://github.com/render-examples/django.git",
        "serviceDetails": {
            "plan": "free",  # Free plan
            "runtime": "python",
            "envSpecificDetails": {
                "buildCommand": "./build.sh",
                "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker"
            },
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
    
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        service_info = response.json()
        print("✓ FREE Web servisi başarıyla oluşturuldu!")
        print(json.dumps(service_info, indent=2))
        return service_info
    else:
        print(f"Web servisi oluşturma hatası:")
        print(f"Response: {response.text}")
        return None

def create_ultra_minimal():
    print("\nUltra minimal konfigürasyonla deniyoruz...")
    
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    
    service_data = {
        "name": "cesa-minimal",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "repo": "https://github.com/render-examples/django.git",
        "serviceDetails": {
            "envSpecificDetails": {
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python manage.py runserver 0.0.0.0:$PORT"
            }
        }
    }
    
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    print(f"Ultra Minimal Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    create_free_web_service()
    create_ultra_minimal() 