import requests
import json
import uuid
import base64

# GitHub bilgileri
GITHUB_USERNAME = "ismailcaprak23"
GITHUB_EMAIL = "ismailcaprak23@gmail.com" 
GITHUB_PASSWORD = "Alozikaos5621?"
REPO_NAME = "cesa-hukuk-burosu"

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

def create_github_repo():
    print("GitHub repository oluşturuluyor...")
    
    # GitHub API ile repo oluştur
    auth = base64.b64encode(f"{GITHUB_USERNAME}:{GITHUB_PASSWORD}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repo_data = {
        "name": REPO_NAME,
        "description": "CESA Hukuk Bürosu - Professional Law Firm Website",
        "private": False,  # Public repo (Render free plan için gerekli)
        "auto_init": False
    }
    
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json=repo_data
    )
    
    if response.status_code == 201:
        repo_info = response.json()
        print(f"✓ GitHub repository başarıyla oluşturuldu: {repo_info['html_url']}")
        return repo_info
    else:
        print(f"GitHub repo oluşturma hatası: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_render_service_with_github():
    print("Render web servisi GitHub repo ile oluşturuluyor...")
    
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    service_data = {
        "name": "cesa-hukuk-burosu",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "repo": f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}",
        "branch": "master",
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
    
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    print(f"Render Service Status: {response.status_code}")
    if response.status_code == 201:
        service_info = response.json()
        print("✓ Render web servisi başarıyla oluşturuldu!")
        print(json.dumps(service_info, indent=2))
        return service_info
    else:
        print(f"Render service oluşturma hatası:")
        print(f"Response: {response.text}")
        return None

def main():
    print("=== CESA Hukuk Bürosu Deployment Başlatılıyor ===\n")
    
    # 1. GitHub repo oluştur
    repo_info = create_github_repo()
    if not repo_info:
        print("❌ GitHub repo oluşturulamadı, işlem durduruluyor.")
        return
    
    print(f"\n📋 Sonraki adımlar:")
    print(f"1. Git remote ekle: git remote add origin {repo_info['clone_url']}")
    print(f"2. Kodu push et: git push -u origin master")
    print(f"3. Render'da servis oluştur")
    
    input("\nGitHub'a kodu push ettikten sonra ENTER'a basın...")
    
    # 2. Render'da servis oluştur
    service_info = create_render_service_with_github()
    
    if service_info:
        print(f"\n🎉 Deployment tamamlandı!")
        print(f"🌐 Website URL: https://{service_info['service']['name']}.onrender.com")
    else:
        print(f"\n⚠️  Render servisi oluşturulamadı. Manuel olarak oluşturmanız gerekebilir.")

if __name__ == "__main__":
    main() 