import requests
import json

# Render API bilgileri
API_KEY = "rnd_uzQg8XKYy9umEbnYgSlQcU6dq9DL"
API_URL = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def list_services():
    print("🔍 Mevcut servisleri listeliyorum...")
    
    response = requests.get(
        f"{API_URL}/services",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        services = response.json()
        print(f"✅ {len(services)} servis bulundu:")
        
        for service in services:
            print(f"\n📋 Service:")
            print(f"  - ID: {service.get('id')}")
            print(f"  - Name: {service.get('name')}")
            print(f"  - Type: {service.get('type')}")
            print(f"  - Status: {service.get('serviceDetails', {}).get('deployStatus', 'N/A')}")
            print(f"  - URL: {service.get('serviceDetails', {}).get('url', 'N/A')}")
            
            # CESA Hukuk servisi ise environment variables'ları göster
            if 'cesa' in service.get('name', '').lower():
                print(f"  - 🎯 CESA Hukuk servisi bulundu!")
                show_env_vars(service.get('id'))
        
        return services
    else:
        print(f"❌ Servisler listelenemedi: {response.status_code}")
        print(f"Response: {response.text}")
        return []

def show_env_vars(service_id):
    print(f"\n🔧 Service {service_id} environment variables:")
    
    response = requests.get(
        f"{API_URL}/services/{service_id}/env-vars",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        env_vars = response.json()
        for env_var in env_vars:
            key = env_var.get('key')
            value = env_var.get('value', '')
            
            # DATABASE_URL'yi maskele
            if key == 'DATABASE_URL':
                masked_value = value[:30] + "..." if len(value) > 30 else value
                print(f"  🗄️  {key}: {masked_value}")
                
                # Internal host name var mı kontrol et
                if '.internal' in value:
                    print(f"  ⚠️  SORUN: Internal database URL kullanılıyor!")
                    print(f"  🔧 External URL'ye güncellenmeli")
            else:
                print(f"  🔑 {key}: {value[:20]}..." if len(value) > 20 else f"  🔑 {key}: {value}")
    else:
        print(f"❌ Environment variables alınamadı: {response.status_code}")

def get_external_db_url():
    print("\n🔍 Doğru external database URL'sini belirliyorum...")
    
    # Render'da PostgreSQL external URL formatı genellikle:
    # postgres://user:password@hostname-a.region-postgres.render.com/database
    
    db_id = "dpg-d12nacumcj7s73fhvq2g-a"
    db_user = "cesa_db_user"
    db_name = "cesa_db"
    db_password = "postgres"  # Genellikle default password
    
    # External hostname formatları
    possible_hostnames = [
        f"{db_id}-a.oregon-postgres.render.com",
        f"{db_id}-a.frankfurt-postgres.render.com", 
        f"{db_id}.oregon-postgres.render.com",
        f"{db_id}.frankfurt-postgres.render.com"
    ]
    
    print("🎯 Olası external database URL'leri:")
    for hostname in possible_hostnames:
        external_url = f"postgres://{db_user}:{db_password}@{hostname}/{db_name}"
        print(f"  📋 {external_url}")
    
    return f"postgres://{db_user}:{db_password}@{possible_hostnames[1]}/{db_name}"

def update_database_url(service_id, new_database_url):
    print(f"\n🔧 Service {service_id} DATABASE_URL güncelleniyor...")
    
    # Önce mevcut environment variables'ları al
    response = requests.get(
        f"{API_URL}/services/{service_id}/env-vars",
        headers=HEADERS
    )
    
    if response.status_code != 200:
        print(f"❌ Environment variables alınamadı: {response.status_code}")
        return False
    
    env_vars = response.json()
    
    # DATABASE_URL'yi bul ve güncelle
    for env_var in env_vars:
        if env_var.get('key') == 'DATABASE_URL':
            env_var_id = env_var.get('id')
            
            # Environment variable'ı güncelle
            update_data = {
                "value": new_database_url
            }
            
            update_response = requests.patch(
                f"{API_URL}/services/{service_id}/env-vars/{env_var_id}",
                headers=HEADERS,
                json=update_data
            )
            
            if update_response.status_code == 200:
                print(f"✅ DATABASE_URL başarıyla güncellendi!")
                print(f"🔄 Servis yeniden deploy edilecek...")
                return True
            else:
                print(f"❌ DATABASE_URL güncellenemedi: {update_response.status_code}")
                print(f"Response: {update_response.text}")
                return False
    
    print(f"❌ DATABASE_URL environment variable bulunamadı")
    return False

def main():
    print("=== CESA Hukuk Database URL Düzeltme ===\n")
    
    # 1. Servisleri listele
    services = list_services()
    
    # 2. External database URL'yi belirle
    external_db_url = get_external_db_url()
    
    # 3. CESA Hukuk servisini bul ve güncelle
    for service in services:
        if 'cesa' in service.get('name', '').lower():
            service_id = service.get('id')
            print(f"\n🎯 CESA Hukuk servisi bulundu: {service_id}")
            
            # DATABASE_URL'yi güncelle
            success = update_database_url(service_id, external_db_url)
            
            if success:
                print(f"\n🎉 İşlem tamamlandı!")
                print(f"🔄 Serviste otomatik redeploy başlayacak")
                print(f"📊 Deploy durumunu şuradan takip edebilirsiniz:")
                print(f"   https://dashboard.render.com/web/{service_id}")
            break
    else:
        print(f"\n⚠️  CESA Hukuk servisi bulunamadı")
        print(f"📋 Manuel olarak DATABASE_URL'yi şu değerle güncelleyin:")
        print(f"   {external_db_url}")

if __name__ == "__main__":
    main() 