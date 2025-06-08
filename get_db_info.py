import requests
import time

# Render API bilgileri
API_KEY = "rnd_iwBkK14XhwST3eQ3vGBtrq3BWU51"
API_URL = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Veritabanı ID'si (önceki adımdan alınan)
DB_ID = "dpg-d12nacumcj7s73fhvq2g-a"  # Kendi veritabanı ID'nizi kullanın

def get_database_info():
    print(f"Veritabanı bilgileri alınıyor... ID: {DB_ID}")
    
    response = requests.get(
        f"{API_URL}/postgres/{DB_ID}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        db_info = response.json()
        print("Veritabanı bilgileri:")
        print(json.dumps(db_info, indent=2))
        
        # Bağlantı bilgilerini almaya çalış
        print("\nVeirtabanı bağlantı bilgileri almayı deniyorum...")
        get_connection_strings()
    else:
        print(f"Hata: {response.text}")

def get_connection_strings():
    response = requests.get(
        f"{API_URL}/postgres/{DB_ID}/connection-strings",
        headers=HEADERS
    )
    
    print(f"Connection Strings Status: {response.status_code}")
    if response.status_code == 200:
        conn_info = response.json()
        print("Bağlantı bilgileri:")
        print(json.dumps(conn_info, indent=2))
    else:
        print(f"Bağlantı bilgileri alınamadı: {response.text}")
        
        # Alternatif endpoint deneme
        response = requests.get(
            f"{API_URL}/postgres/{DB_ID}/config",
            headers=HEADERS
        )
        
        print(f"\nConfig Status: {response.status_code}")
        if response.status_code == 200:
            config_info = response.json()
            print("Yapılandırma bilgileri:")
            print(json.dumps(config_info, indent=2))
        else:
            print(f"Yapılandırma bilgileri alınamadı: {response.text}")

if __name__ == "__main__":
    import json
    get_database_info() 