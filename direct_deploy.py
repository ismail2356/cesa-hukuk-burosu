import requests
import json
import uuid
import base64
import os

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

def create_service_with_static_site():
    print("Static site olarak deploy deneniyor...")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    # Static site olarak oluştur
    service_data = {
        "name": "cesa-hukuk",
        "ownerId": OWNER_ID,
        "type": "static_site",
        "region": "frankfurt",
        "buildCommand": "./build.sh",
        "publishPath": ".",
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
            }
        ]
    }
    
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    print(f"Static Site Status: {response.status_code}")
    print(f"Response: {response.text}")

def explore_api_endpoints():
    print("Mevcut API endpoint'lerini keşfediyoruz...")
    
    # Farklı endpoint'leri test et
    endpoints = [
        "/",
        "/docs",
        "/openapi.json",
        "/services",
        "/postgres",
        "/owners",
        "/deploys"
    ]
    
    for endpoint in endpoints:
        print(f"\nTest ediliyor: {endpoint}")
        response = requests.get(
            f"{API_URL}{endpoint}",
            headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Type: {type(data)}")
                if isinstance(data, dict) and len(data) < 10:
                    print(f"Keys: {list(data.keys())}")
                elif isinstance(data, list) and len(data) == 0:
                    print("Empty list")
                elif isinstance(data, str) and len(data) < 500:
                    print(f"Content: {data[:200]}...")
            except:
                print(f"Raw response: {response.text[:200]}...")

def try_github_approach():
    print("\nGitHub repo yaklaşımını deniyoruz...")
    
    # Rastgele bir SECRET_KEY oluştur
    secret_key = f"django-insecure-{uuid.uuid4().hex}"
    db_connection_string = f"postgres://{DB_USER}:postgres@{DB_ID}.internal:5432/{DB_NAME}"
    
    # GitHub repo ile deneme
    service_data = {
        "name": "cesa-hukuk",
        "ownerId": OWNER_ID,
        "type": "web_service",
        "region": "frankfurt",
        "repo": "https://github.com/placeholder/placeholder",  # Placeholder repo
        "branch": "main",
        "buildCommand": "./build.sh",
        "startCommand": "gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker",
        "runtime": "python",
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
    
    response = requests.post(
        f"{API_URL}/services",
        headers=HEADERS,
        json=service_data
    )
    
    print(f"GitHub Approach Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    explore_api_endpoints()
    create_service_with_static_site()
    try_github_approach() 