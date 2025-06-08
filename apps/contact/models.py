from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    """İletişim mesajı modeli"""
    full_name = models.CharField('Ad Soyad', max_length=100)
    email = models.EmailField('E-posta')
    phone = models.CharField('Telefon', max_length=20, blank=True, null=True)
    subject = models.CharField('Konu', max_length=200)
    message = models.TextField('Mesaj')
    is_read = models.BooleanField('Okundu', default=False)
    created_at = models.DateTimeField('Gönderim Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'İletişim Mesajı'
        verbose_name_plural = 'İletişim Mesajları'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

class OfficeLocation(models.Model):
    """Ofis lokasyonu modeli"""
    name = models.CharField('Lokasyon Adı', max_length=100)
    address = models.TextField('Adres')
    phone = models.CharField('Telefon', max_length=20)
    email = models.EmailField('E-posta', blank=True, null=True)
    google_maps_link = models.URLField('Google Maps Linki', blank=True, null=True)
    google_maps_embed = models.TextField('Google Maps Embed Kodu', blank=True, null=True)
    is_main = models.BooleanField('Ana Ofis', default=False)
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveIntegerField('Sıralama', default=0)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Ofis Lokasyonu'
        verbose_name_plural = 'Ofis Lokasyonları'
        ordering = ['order']

    def __str__(self):
        return self.name
