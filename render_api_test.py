import requests
import json

def test_render_api():
    api_key = "rnd_iwBkK14XhwST3eQ3vGBtrq3BWU51"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Kullanıcı bilgilerini almaya çalış
    print("1. Kullanıcı bilgilerini alınıyor...")
    response = requests.get(
        "https://api.render.com/v1/users/me",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)
    
    # Servisleri listelemeyi dene
    print("2. Servisler listeleniyor...")
    response = requests.get(
        "https://api.render.com/v1/services",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)
    
    # Kullanıcı hesap bilgilerini alma
    print("3. Hesap bilgileri alınıyor...")
    response = requests.get(
        "https://api.render.com/v1/owners",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    test_render_api() 