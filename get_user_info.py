import os
import requests
import json

# Render API bilgileri
API_KEY = os.environ.get('RENDER_API_KEY', 'rnd_iwBkK14XhwST3eQ3vGBtrq3BWU51')
API_URL = 'https://api.render.com/v1'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Kullanıcı bilgilerini al
def get_user_info():
    response = requests.get(
        f'{API_URL}/users/me',
        headers=HEADERS
    )
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        user_info = response.json()
        print("\nKullanıcı Bilgileri:")
        print(f"ID: {user_info.get('id')}")
        print(f"Email: {user_info.get('email')}")
        
        # Çalışma alanlarını listele
        list_workspaces()
    else:
        print("Kullanıcı bilgileri alınamadı.")

# Çalışma alanlarını listele
def list_workspaces():
    response = requests.get(
        f'{API_URL}/workspaces',
        headers=HEADERS
    )
    
    print(f"\nWorkspaces Status code: {response.status_code}")
    
    if response.status_code == 200:
        workspaces = response.json()
        print("\nÇalışma Alanları:")
        for ws in workspaces:
            print(f"ID: {ws.get('id')}, Ad: {ws.get('name')}")
    else:
        print(f"Çalışma alanları listelenemiyor: {response.text}")

if __name__ == "__main__":
    get_user_info() 