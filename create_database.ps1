# PostgreSQL veritabanı oluşturma PowerShell betiği
Write-Host "PostgreSQL veritabanı oluşturuluyor..." -ForegroundColor Green

# PostgreSQL yolu ve kimlik bilgileri
$pgPassword = "123456"
$pgUser = "postgres"
$pgDatabase = "cesa_hukuk"

# PostgreSQL yolu - standart kurulum yolları
$pgBinPaths = @(
    "C:\Program Files\PostgreSQL\16\bin",
    "C:\Program Files\PostgreSQL\15\bin",
    "C:\Program Files\PostgreSQL\14\bin",
    "C:\Program Files\PostgreSQL\13\bin",
    "C:\Program Files\PostgreSQL\12\bin"
)

$psqlPath = $null
foreach ($path in $pgBinPaths) {
    if (Test-Path "$path\psql.exe") {
        $psqlPath = "$path\psql.exe"
        break
    }
}

if ($psqlPath -eq $null) {
    Write-Host "HATA: psql.exe bulunamadı. PostgreSQL'in bin dizinini ekleyin." -ForegroundColor Red
    Write-Host "Olası dizinler: $($pgBinPaths -join ', ')" -ForegroundColor Yellow
    exit
}

# SQL komutlarını doğrudan çalıştır
Write-Host "PostgreSQL kullanılıyor: $psqlPath" -ForegroundColor Cyan
$env:PGPASSWORD = $pgPassword

# Veritabanı oluştur
Write-Host "Veritabanı siliniyor (varsa)..." -ForegroundColor Yellow
& $psqlPath -U $pgUser -c "DROP DATABASE IF EXISTS $pgDatabase;"

Write-Host "Yeni veritabanı oluşturuluyor..." -ForegroundColor Green
& $psqlPath -U $pgUser -c "CREATE DATABASE $pgDatabase WITH ENCODING 'UTF8';"

# Tamamlandı
Write-Host "`nVeritabanı başarıyla oluşturuldu!" -ForegroundColor Green
Write-Host "`nŞimdi migrasyonları çalıştırın:" -ForegroundColor Green
Write-Host "python manage.py migrate" -ForegroundColor Cyan

Write-Host "`nSonra admin kullanıcısını oluşturun:" -ForegroundColor Green
Write-Host "python create_admin.py" -ForegroundColor Cyan

# Bekleme
Write-Host "`nDevam etmek için bir tuşa basın..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 