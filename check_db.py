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

def get_databases():
    print("Veritabanları alınıyor...")
    
    response = requests.get(
        f"{API_URL}/postgres",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        try:
            databases = response.json()
            print(f"Toplam veritabanı sayısı: {len(databases)}")
            print(f"Raw response: {response.text}")
            
            # Tam yanıtı ayrıştır
            for i, db in enumerate(databases, 1):
                print(f"\nDB {i} Detayları:")
                for key, value in db.items():
                    print(f"  {key}: {value}")
                
                # Önemli veritabanı bilgilerini al
                db_id = db.get("id")
                if db_id:
                    get_db_details(db_id)
        except Exception as e:
            print(f"JSON ayrıştırma hatası: {e}")
            print(f"Raw response: {response.text}")
    else:
        print(f"Hata: {response.text}")

def get_db_details(db_id):
    print(f"\nVeritabanı detayları alınıyor... ID: {db_id}")
    
    response = requests.get(
        f"{API_URL}/postgres/{db_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        try:
            db_info = response.json()
            print("Veritabanı detayları:")
            print(json.dumps(db_info, indent=2))
        except Exception as e:
            print(f"JSON ayrıştırma hatası: {e}")
            print(f"Raw response: {response.text}")
    else:
        print(f"Hata: {response.text}")

if __name__ == "__main__":
    get_databases() 