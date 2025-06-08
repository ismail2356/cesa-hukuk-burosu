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

def create_web_service_proper():
    print("Düzgün formatla web servisi oluşturuluyor...")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    # Doğru format ile web servisi
    service_data = {
        "name": "cesa-hukuk",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "repo": "https://github.com/django/django.git",  # Geçici placeholder repo
        "branch": "main",
        "serviceDetails": {
            "runtime": "python",
            "buildCommand": "./build.sh",
            "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
            "plan": "starter",
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
        
        # Servisi oluşturduktan sonra dosyaları yüklemeye çalış
        service_id = service_info.get("id")
        if service_id:
            upload_files_to_service(service_id)
            
        return service_info
    else:
        print(f"Web servisi oluşturma hatası:")
        print(f"Response: {response.text}")
        return None

def upload_files_to_service(service_id):
    print(f"\nDosyalar service ID'ye yükleniyor: {service_id}")
    
    # Farklı upload endpoint'leri dene
    upload_endpoints = [
        f"{API_URL}/services/{service_id}/files",
        f"{API_URL}/services/{service_id}/upload",
        f"{API_URL}/services/{service_id}/deploy",
        f"{API_URL}/services/{service_id}/source"
    ]
    
    zip_file_path = "cesa_hukuk_render.zip"
    
    for endpoint in upload_endpoints:
        print(f"Deneniyor: {endpoint}")
        
        try:
            with open(zip_file_path, 'rb') as f:
                files = {'file': ('cesa_hukuk_render.zip', f, 'application/zip')}
                
                response = requests.post(
                    endpoint,
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    files=files
                )
                
                print(f"  Status: {response.status_code}")
                print(f"  Response: {response.text[:200]}...")
                
                if response.status_code in [200, 201, 202]:
                    print("  ✓ Başarılı!")
                    return True
        except Exception as e:
            print(f"  Hata: {e}")
    
    return False

def try_direct_deploy():
    print("\nDirekt deploy endpoint'ini deniyoruz...")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    deploy_data = {
        "service": {
            "name": "cesa-hukuk",
            "ownerId": OWNER_ID,
            "type": "web_service",
            "region": "frankfurt",
            "serviceDetails": {
                "runtime": "python",
                "buildCommand": "./build.sh",
                "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
                "plan": "starter",
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
    }
    
    # Dosya ile birlikte gönder
    zip_file_path = "cesa_hukuk_render.zip"
    
    try:
        with open(zip_file_path, 'rb') as f:
            files = {
                'file': ('cesa_hukuk_render.zip', f, 'application/zip'),
                'data': (None, json.dumps(deploy_data), 'application/json')
            }
            
            response = requests.post(
                f"{API_URL}/services",
                headers={"Authorization": f"Bearer {API_KEY}"},
                files=files
            )
            
            print(f"Direct Deploy Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Direct deploy hatası: {e}")

if __name__ == "__main__":
    create_web_service_proper()
    try_direct_deploy() 