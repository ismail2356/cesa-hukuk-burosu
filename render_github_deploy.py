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

# GitHub repository bilgisi
GITHUB_REPO = "https://github.com/ismail2356/cesa-hukuk-burosu"

def create_render_service():
    print("🚀 Render web servisi oluşturuluyor...")
    
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    print(f"📊 Kullanılacak bilgiler:")
    print(f"  - GitHub Repo: {GITHUB_REPO}")
    print(f"  - Database: {db_connection_string}")
    print(f"  - Secret Key: {secret_key[:20]}...")
    
    service_data = {
        "name": "cesa-hukuk-burosu",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "repo": GITHUB_REPO,
        "branch": "master",
        "serviceDetails": {
            "runtime": "python",
            "plan": "starter",
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
    
    print("\n📤 Render API'sine istek gönderiliyor...")
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    print(f"📊 Response Status: {response.status_code}")
    
    if response.status_code == 201:
        service_info = response.json()
        print("✅ Render web servisi başarıyla oluşturuldu!")
        print(f"🌐 Service URL: https://{service_info['service']['name']}.onrender.com")
        print(f"📝 Service ID: {service_info['service']['id']}")
        print(f"🎯 Deploy Status: {service_info['service']['serviceDetails']['deployStatus']}")
        return service_info
    elif response.status_code == 402:
        print("💳 Ödeme gerekli - Starter plan için kredi kartı bilgisi gerekiyor")
        print("🔄 Free plan ile deneniyor...")
        return try_free_plan()
    else:
        print(f"❌ Render service oluşturma hatası:")
        print(f"📄 Response: {response.text}")
        return None

def try_free_plan():
    print("\n🆓 Free plan ile deneniyor...")
    
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    service_data = {
        "name": "cesa-hukuk-free",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "repo": GITHUB_REPO,
        "branch": "master",
        "serviceDetails": {
            "runtime": "python",
            "plan": "free",
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
    
    print(f"📊 Free Plan Response Status: {response.status_code}")
    
    if response.status_code == 201:
        service_info = response.json()
        print("✅ FREE web servisi başarıyla oluşturuldu!")
        print(f"🌐 Service URL: https://{service_info['service']['name']}.onrender.com")
        return service_info
    else:
        print(f"❌ Free plan da çalışmadı:")
        print(f"📄 Response: {response.text}")
        return None

def main():
    print("=== CESA Hukuk Bürosu - Render Deployment ===\n")
    print(f"🔗 GitHub Repository: {GITHUB_REPO}")
    print(f"📡 Render API Key: {API_KEY[:15]}...")
    print(f"🗄️  Database ID: {DB_ID}")
    
    service_info = create_render_service()
    
    if service_info:
        print(f"\n🎉 DEPLOYMENT BAŞARILI!")
        print(f"🌐 Website URL: https://{service_info['service']['name']}.onrender.com")
        print(f"\n📋 Sonraki adımlar:")
        print(f"1. Render dashboard'da deployment durumunu takip edin")
        print(f"2. Build tamamlandığında website'i test edin")
        print(f"3. Admin panel: https://{service_info['service']['name']}.onrender.com/admin")
        print(f"   - Username: admin")
        print(f"   - Password: Admin123!")
    else:
        print(f"\n⚠️  Manuel deployment gerekiyor:")
        print(f"1. https://dashboard.render.com adresine gidin")
        print(f"2. 'New Web Service' oluşturun")
        print(f"3. GitHub repo: {GITHUB_REPO}")
        print(f"4. Build Command: ./build.sh")
        print(f"5. Start Command: gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker")
        print(f"6. Environment variables'ları ekleyin")

if __name__ == "__main__":
    main() 