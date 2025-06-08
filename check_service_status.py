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

def check_service_status():
    print("🔍 Service durumu kontrol ediliyor...")
    
    response = requests.get(
        f"{API_URL}/services",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        services = response.json()
        
        for service in services:
            name = service.get('name', 'Unknown')
            if 'cesa' in name.lower():
                print(f"\n🎯 CESA Service bulundu:")
                print(f"  📋 Name: {name}")
                print(f"  🆔 ID: {service.get('id')}")
                print(f"  🌐 URL: https://{name}.onrender.com")
                
                service_details = service.get('serviceDetails', {})
                print(f"  📊 Deploy Status: {service_details.get('deployStatus', 'Unknown')}")
                print(f"  🔄 Health Status: {service_details.get('healthStatus', 'Unknown')}")
                print(f"  ⏰ Created: {service.get('createdAt', 'Unknown')}")
                print(f"  🔄 Updated: {service.get('updatedAt', 'Unknown')}")
                
                # Deploy geçmişini kontrol et
                service_id = service.get('id')
                if service_id:
                    check_deploys(service_id)
                
                return service
    else:
        print(f"❌ Services alınamadı: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def check_deploys(service_id):
    print(f"\n📋 Deploy geçmişi kontrol ediliyor... (Service ID: {service_id})")
    
    response = requests.get(
        f"{API_URL}/services/{service_id}/deploys",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        deploys = response.json()
        
        if deploys:
            latest_deploy = deploys[0]  # En son deploy
            print(f"\n🚀 Son Deploy:")
            print(f"  🆔 Deploy ID: {latest_deploy.get('id')}")
            print(f"  📊 Status: {latest_deploy.get('status')}")
            print(f"  ⏰ Created: {latest_deploy.get('createdAt')}")
            print(f"  🔄 Updated: {latest_deploy.get('updatedAt')}")
            
            if latest_deploy.get('status') == 'build_failed':
                print(f"  ❌ SORUN: Build başarısız!")
            elif latest_deploy.get('status') == 'live':
                print(f"  ✅ Deploy başarılı ve canlı!")
            else:
                print(f"  ⏳ Deploy durumu: {latest_deploy.get('status')}")
        else:
            print("  ❌ Deploy geçmişi bulunamadı")
    else:
        print(f"❌ Deploy bilgileri alınamadı: {response.status_code}")

def test_website():
    print(f"\n🌐 Website erişilebilirlik testi...")
    
    test_urls = [
        "https://cesa-hukuk-burosu.onrender.com",
        "https://cesa-hukuk-burosu.onrender.com/admin",
        "https://cesa-hukuk-burosu.onrender.com/about",
    ]
    
    for url in test_urls:
        print(f"\n🔗 Test ediliyor: {url}")
        try:
            response = requests.get(url, timeout=30)
            print(f"  📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Başarılı!")
                print(f"  📄 Content Length: {len(response.content)} bytes")
            elif response.status_code == 404:
                print(f"  ❌ Not Found (404)")
            elif response.status_code == 500:
                print(f"  ❌ Server Error (500)")
            else:
                print(f"  ⚠️  HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Bağlantı hatası: {e}")

def main():
    print("=== CESA Hukuk Service Durum Kontrolü ===\n")
    
    # 1. Service durumunu kontrol et
    service = check_service_status()
    
    # 2. Website erişilebilirlik testi
    test_website()
    
    print(f"\n📋 Öneriler:")
    print(f"1. Render Dashboard'ı kontrol edin: https://dashboard.render.com")
    print(f"2. Service logs'unu inceleyin")
    print(f"3. Deploy işleminin tamamlanmasını bekleyin")
    print(f"4. DNS propagation için 5-10 dakika bekleyin")

if __name__ == "__main__":
    main() 