import requests
import json

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

# Veritabanlarını listele
def list_databases(owner_id):
    print("\nVeritabanları listeleniyor...")
    
    response = requests.get(
        f"{API_URL}/postgres",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        databases = response.json()
        if not databases:
            print("Hiç veritabanı bulunamadı.")
            return
        
        for i, db in enumerate(databases, 1):
            print(f"\n{i}. Veritabanı:")
            print(f"   ID: {db.get('id')}")
            print(f"   İsim: {db.get('name')}")
            print(f"   Durum: {db.get('status')}")
            print(f"   Plan: {db.get('plan')}")
            print(f"   Bölge: {db.get('region')}")
            print(f"   Kullanıcı: {db.get('databaseUser')}")
            print(f"   Veritabanı Adı: {db.get('databaseName')}")
    else:
        print(f"Veritabanları listelenemedi: {response.status_code}")
        print(f"Hata: {response.text}")

# Servisleri listele
def list_services(owner_id):
    print("\nServisler listeleniyor...")
    
    response = requests.get(
        f"{API_URL}/services",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        services = response.json()
        if not services:
            print("Hiç servis bulunamadı.")
            return
        
        for i, service_data in enumerate(services, 1):
            service = service_data.get("service", {})
            print(f"\n{i}. Servis:")
            print(f"   ID: {service_data.get('id')}")
            print(f"   İsim: {service.get('name')}")
            print(f"   Tür: {service.get('type')}")
            print(f"   Durum: {service.get('suspended')}")
            print(f"   Bölge: {service.get('region')}")
            
            # Servisin URL'si
            service_details = service.get("serviceDetails", {})
            url = service_details.get("url")
            if url:
                print(f"   URL: {url}")
    else:
        print(f"Servisler listelenemedi: {response.status_code}")
        print(f"Hata: {response.text}")

if __name__ == "__main__":
    owner_id = get_owner_id()
    if owner_id:
        list_databases(owner_id)
        list_services(owner_id) 