import os
import requests
import json
import time
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

# Render üzerinde PostgreSQL veritabanı oluşturma
def create_database(owner_id):
    print("PostgreSQL veritabanı oluşturuluyor...")
    
    # Önce mevcut veritabanlarını kontrol et
    print("Mevcut veritabanları kontrol ediliyor...")
    response = requests.get(
        f"{API_URL}/postgres?ownerId={owner_id}",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        databases = response.json()
        for db in databases:
            if db.get("name") == "cesa-db":
                print(f"Veritabanı zaten mevcut! ID: {db.get('id')}")
                return db
    
    # Yeni veritabanı oluştur
    db_data = {
        "name": "cesa-db",
        "region": "frankfurt",  # Lokasyonu değiştirebilirsiniz
        "plan": "free",  # Ücretsiz plan
        "isPublic": False,
        "user": "cesa_user",
        "database": "cesa_hukuk",
        "ownerId": owner_id,
        "version": "15"  # PostgreSQL sürümü
    }
    
    response = requests.post(
        f"{API_URL}/postgres",
        headers=HEADERS,
        json=db_data
    )
    
    if response.status_code == 201:
        db_info = response.json()
        print(f"Veritabanı başarıyla oluşturuldu! ID: {db_info.get('id')}")
        return db_info
    else:
        print(f"Veritabanı oluşturma hatası: {response.status_code}")
        print(f"Hata mesajı: {response.text}")
        return None

# Veritabanı durumunu kontrol et
def wait_for_database_ready(db_id, max_attempts=30):
    print(f"Veritabanının hazır olması bekleniyor... ID: {db_id}")
    attempts = 0
    
    while attempts < max_attempts:
        response = requests.get(
            f"{API_URL}/postgres/{db_id}",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            db_info = response.json()
            status = db_info.get("status")
            print(f"Veritabanı durumu: {status}")
            
            if status == "live":
                print("Veritabanı hazır!")
                # PostgreSQL'in tam olarak hazır olması için biraz daha bekle
                time.sleep(5)
                return db_info
            elif status == "error":
                print("Veritabanı oluşturulurken hata oluştu.")
                return None
        
        print(f"Bekleniyor... ({attempts + 1}/{max_attempts})")
        attempts += 1
        time.sleep(10)  # 10 saniye bekle
    
    print("Veritabanı hazır olmadı. Zaman aşımı.")
    return None

# Veritabanı bağlantı bilgilerini oluştur
def generate_database_connection_string(db_info):
    print("Veritabanı bağlantı bilgileri oluşturuluyor...")
    
    db_name = db_info.get("databaseName", "cesa_hukuk")
    db_user = db_info.get("databaseUser", "cesa_user")
    region = db_info.get("region", "frankfurt")
    db_id = db_info.get("id")
    
    # Render'ın iç ağında kullanılan format
    connection_string = f"postgres://{db_user}:postgres@{db_id}.internal:5432/{db_name}"
    print(f"Oluşturulan bağlantı dizesi: {connection_string}")
    
    return connection_string

# Web service oluşturma
def create_web_service(owner_id, db_connection_string):
    print("Web servisi oluşturuluyor...")
    
    # Önce mevcut servisleri kontrol et
    print("Mevcut servisler kontrol ediliyor...")
    response = requests.get(
        f"{API_URL}/services?ownerId={owner_id}",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        services = response.json()
        for service in services:
            service_name = service.get("service", {}).get("name")
            if service_name == "cesa-hukuk":
                service_id = service.get("id")
                print(f"Web servisi zaten mevcut! ID: {service_id}")
                return service
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    
    service_data = {
        "type": "web_service",
        "name": "cesa-hukuk",
        "ownerId": owner_id,
        "region": "frankfurt",
        "plan": "starter",
        "runtime": "python",
        "buildCommand": "./build.sh",
        "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
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
                "value": "Admin123!"  # Gerçek deploymentta daha güçlü bir parola kullanın!
            },
            {
                "key": "PORT",
                "value": "10000"
            }
        ]
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

# Manuel deploy trigger etme
def trigger_deploy(service_id):
    print(f"Deploy tetikleniyor... Service ID: {service_id}")
    
    response = requests.post(
        f"{API_URL}/services/{service_id}/deploys",
        headers=HEADERS
    )
    
    if response.status_code == 201:
        deploy_info = response.json()
        print(f"Deploy başarıyla tetiklendi! Deploy ID: {deploy_info.get('id')}")
        return deploy_info
    else:
        print(f"Deploy tetikleme hatası: {response.status_code}")
        print(f"Hata mesajı: {response.text}")
        return None

# Ana fonksiyon
def deploy_to_render():
    print("CESA Hukuk Bürosu projesi Render'a deploy ediliyor...")
    
    # 1. Owner ID'yi al
    owner_id = get_owner_id()
    if not owner_id:
        print("Owner ID alınamadı. İşlem durduruldu.")
        return
    
    # 2. Veritabanı oluştur
    db_info = create_database(owner_id)
    if not db_info:
        print("Veritabanı oluşturulamadı. İşlem durduruldu.")
        return
    
    # 3. Veritabanının hazır olmasını bekle
    db_id = db_info.get("id")
    db_ready_info = wait_for_database_ready(db_id)
    if not db_ready_info:
        print("Veritabanı hazır olmadı. İşlem durduruldu.")
        return
    
    # 4. Veritabanı bağlantı bilgilerini oluştur
    db_connection_string = generate_database_connection_string(db_ready_info)
    if not db_connection_string:
        print("Veritabanı bağlantı bilgileri oluşturulamadı. İşlem durduruldu.")
        return
    
    # 5. Web servisi oluştur
    service_info = create_web_service(owner_id, db_connection_string)
    if not service_info:
        print("Web servisi oluşturulamadı. İşlem durduruldu.")
        return
    
    # 6. Deploy tetikle
    service_id = service_info.get("id")
    if service_id:
        trigger_deploy(service_id)
    
    print("\n=== Deploy İşlemi Başarıyla Tamamlandı ===")
    print("Web siteniz birkaç dakika içinde hazır olacak.")
    print("Admin paneline giriş yapmak için:")
    print("Kullanıcı adı: admin")
    print("Şifre: Admin123!")
    print("\nÖzel alan adınızı bağlamak için Render dashboard'a gidin ve Custom Domain ekleyin.")

if __name__ == "__main__":
    deploy_to_render() 