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

def get_service_id():
    print("🔍 Service ID'si alınıyor...")
    
    response = requests.get(
        f"{API_URL}/services",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        services = response.json()
        
        for service in services:
            name = service.get('name', 'Unknown')
            if 'cesa' in name.lower():
                service_id = service.get('id')
                print(f"✅ Service bulundu: {name} (ID: {service_id})")
                return service_id
    
    print("❌ CESA service bulunamadı!")
    return None

def trigger_deploy(service_id):
    print(f"🚀 Manuel deploy tetikleniyor... (Service ID: {service_id})")
    
    deploy_data = {
        "clearCache": "clear"
    }
    
    response = requests.post(
        f"{API_URL}/services/{service_id}/deploys",
        headers=HEADERS,
        json=deploy_data
    )
    
    if response.status_code == 201:
        deploy = response.json()
        deploy_id = deploy.get('id')
        status = deploy.get('status')
        
        print(f"✅ Deploy başarıyla tetiklendi!")
        print(f"  🆔 Deploy ID: {deploy_id}")
        print(f"  📊 Status: {status}")
        print(f"  ⏰ Created: {deploy.get('createdAt')}")
        
        print(f"\n📋 Deploy takibi:")
        print(f"1. Render Dashboard: https://dashboard.render.com")
        print(f"2. Service logs'unu izleyin")
        print(f"3. Deploy tamamlandığında website'i test edin: https://cesa-hukuk-burosu.onrender.com")
        
        return deploy_id
    else:
        print(f"❌ Deploy tetiklenemedi: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    print("=== RENDER MANUEL DEPLOY ===\n")
    
    # 1. Service ID'sini al
    service_id = get_service_id()
    
    if service_id:
        # 2. Deploy tetikle
        deploy_id = trigger_deploy(service_id)
        
        if deploy_id:
            print(f"\n🎉 Deploy başlatıldı! 2-3 dakika içinde tamamlanacak.")
            print(f"📋 Takip için: https://dashboard.render.com")
        else:
            print(f"\n❌ Deploy başlatılamadı.")
    else:
        print(f"\n❌ Service bulunamadı.")

if __name__ == "__main__":
    main() 