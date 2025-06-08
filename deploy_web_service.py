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

# Owner ID'yi al
def get_owner_id():
    print("Hesap bilgileri alınıyor...")
    
    response = requests.get(
        f"{API_URL}/owners",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        owners = response.json()
        if owners and len(owners) > 0:
            owner = owners[0].get("owner", {})
            owner_id = owner.get("id")
            if owner_id:
                print(f"Owner ID: {owner_id}")
                return owner_id
    
    print("Owner ID alınamadı!")
    return None

# Web service oluşturma
def create_web_service(owner_id):
    print("Web servisi oluşturuluyor...")
    
    # Render yapılandırmasını biliyoruz
    db_connection_string = "postgres://cesa_db_user:postgres@dpg-d12nacumcj7s73fhvq2g-a.internal:5432/cesa_db"
    print(f"Veritabanı bağlantı dizesi: {db_connection_string}")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    
    service_data = {
        "service": {
            "name": "cesa-hukuk",
            "type": "web_service",
            "ownerID": owner_id,
            "region": "frankfurt",
            "plan": "starter",
            "autoDeploy": "yes",
            "suspended": "not_suspended",
            "serviceDetails": {
                "pullRequestPreviewsEnabled": False,
                "buildCommand": "./build.sh",
                "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
                "runtime": "python",
                "numInstances": 1,
                "pullRequestPreviewsEnvironmentName": "staging",
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
    
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    if response.status_code == 201:
        service_info = response.json()
        service_id = service_info.get("id")
        print(f"Web servisi başarıyla oluşturuldu! ID: {service_id}")
        return service_info
    else:
        print(f"Web servisi oluşturma hatası: {response.status_code}")
        print(f"Hata mesajı: {response.text}")
        return None

if __name__ == "__main__":
    # 1. Owner ID'yi al
    owner_id = get_owner_id()
    if not owner_id:
        print("Owner ID alınamadı. İşlem durduruldu.")
        exit(1)
    
    # 2. Web servisi oluştur
    service_info = create_web_service(owner_id)
    if not service_info:
        print("Web servisi oluşturulamadı. İşlem durduruldu.")
        exit(1)
    
    print("\n=== Web Service Deploy İşlemi Başarıyla Tamamlandı ===")
    print("Web siteniz birkaç dakika içinde hazır olacak.")
    print("Admin paneline giriş yapmak için:")
    print("Kullanıcı adı: admin")
    print("Şifre: Admin123!") 