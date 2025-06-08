# CESA Hukuk Bürosu Web Sitesi

Bu proje, CESA Hukuk Bürosu için geliştirilmiş Django tabanlı bir web sitesini içerir.

## Teknik Özellikler

- **Framework:** Django 4.2.21
- **Veritabanı:** PostgreSQL
- **Frontend:** Bootstrap, AOS Animasyon
- **Responsive:** Tüm cihazlar için tam uyumlu tasarım

## Gereksinimler

- Python 3.9+
- PostgreSQL
- Diğer bağımlılıklar requirements.txt dosyasında listelenmiştir

## Kurulum

1. Sanal ortam oluşturun ve aktifleştirin:
```
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell için
```

2. Bağımlılıkları yükleyin:
```
pip install -r requirements.txt
```

3. Veritabanını hazırlayın:
```
python manage.py migrate
```

4. Sunucuyu başlatın:
```
python manage.py runserver
```

## Render'a Deploy Etme

### Manuel Deploy Adımları

1. Render.com hesabınıza giriş yapın
2. Dashboard'dan "New +" düğmesine tıklayın ve "PostgreSQL" seçin
   - **Name**: cesa-db
   - **Database**: cesa_hukuk
   - **User**: cesa_user
   - **Region**: Frankfurt (size en yakın bölge)
   - **Plan**: Free

3. Veritabanı oluşturulduktan sonra "Internal Database URL" bilgisini not alın

4. Tekrar "New +" düğmesine tıklayın ve "Web Service" seçin
   - **Connect a repository** yerine "Upload" seçeneğini seçerek projeyi ZIP olarak yükleyin
   - **Name**: cesa-hukuk
   - **Runtime**: Python
   - **Build Command**: ./build.sh
   - **Start Command**: python -m gunicorn CESA_Hukuk_Burosu.asgi:application -k uvicorn.workers.UvicornWorker
   
5. Environment değişkenlerini ekleyin:
   - DATABASE_URL: [Veritabanı sayfasından aldığınız Internal Database URL]
   - SECRET_KEY: [Güvenli rastgele bir değer]
   - DEBUG: false
   - ADMIN_USERNAME: [Admin kullanıcı adınız]
   - ADMIN_EMAIL: [E-posta adresiniz]
   - ADMIN_PASSWORD: [Güçlü bir parola]

6. "Create Web Service" düğmesine tıklayın

### Wix Domain'i Yapılandırma

1. Render Dashboard'da Web Service'inize tıklayın
2. "Settings" sekmesine gidin ve "Custom Domain" bölümüne ilerleyin
3. "Add Custom Domain" düğmesine tıklayın ve Wix'ten aldığınız domain adını girin
4. Size verilen CNAME kaydını Wix DNS ayarlarında ekleyin:
   - Wix hesabınıza giriş yapın
   - Domain yönetimine gidin
   - DNS kayıtlarını seçin
   - Yeni bir CNAME kaydı ekleyin:
     - **Host/Name**: www (veya @ ana domain için)
     - **Value/Points to**: Render'ın verdiği alan adı
     - **TTL**: 1 saat (veya varsayılan)

## Proje Yapısı

```
CESA_Hukuk_Burosu/   # Django projesinin ana dizini
apps/               # Uygulama modülleri
  core/             # Temel site ayarları
  lawyers/          # Avukatlar yönetimi
  services/         # Hizmetler yönetimi
  blog/             # Blog yönetimi
  contact/          # İletişim formu
static/             # Statik dosyalar (CSS, JS, resimler)
templates/          # Şablonlar
media/              # Kullanıcı yüklenen dosyalar
```

## Bilinen Sorunlar ve Çözümleri

- **Navbar sabitlenmesi:** Fixed-top sınıfı ve JavaScript scroll kontrolü eklenmiştir.
- **Mobil menü:** Responsive tasarım ve touchable hedefler için CSS optimizasyonları eklenmiştir.

## Bakım ve Yönetim

- Admin paneline `/admin` URL'sinden erişebilirsiniz
- İçerik yönetimi admin paneli üzerinden yapılabilir
- SEO ayarları site ayarları bölümünden yapılandırılabilir

## Lisans

Bu proje özel kullanım içindir ve izinsiz dağıtılamaz. 