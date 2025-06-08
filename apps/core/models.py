from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    """Site geneli ayarlar modeli"""
    site_name = models.CharField(_("Site Adı"), max_length=100)
    logo = models.ImageField(_("Logo"), upload_to="general/", blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to="general/", blank=True, null=True)
    email = models.EmailField(_("E-posta"), blank=True, null=True)
    phone = models.CharField(_("Telefon"), max_length=20, blank=True, null=True)
    address = models.TextField(_("Adres"), blank=True, null=True)
    whatsapp = models.CharField(_("WhatsApp"), max_length=20, blank=True, null=True)
    facebook = models.URLField(_("Facebook"), blank=True, null=True)
    instagram = models.URLField(_("Instagram"), blank=True, null=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True, null=True)
    twitter = models.URLField(_("Twitter"), blank=True, null=True)
    
    # SEO Alanları
    meta_title = models.CharField(_("Meta Başlık"), max_length=200, blank=True, null=True, 
                                help_text=_("Ana sayfa için meta başlık. Boş bırakılırsa site adı kullanılır."))
    meta_description = models.TextField(_("Meta Açıklama"), blank=True, null=True,
                                      help_text=_("Ana sayfa için meta açıklama. 160 karakteri geçmemelidir."))
    meta_keywords = models.TextField(_("Meta Anahtar Kelimeler"), blank=True, null=True,
                                   help_text=_("Virgülle ayrılmış anahtar kelimeler."))
    meta_author = models.CharField(_("Meta Yazar"), max_length=100, blank=True, null=True)
    meta_copyright = models.CharField(_("Meta Telif Hakkı"), max_length=200, blank=True, null=True)
    
    # Analitik ve Doğrulama Kodları
    google_analytics = models.TextField(_("Google Analytics Kodu"), blank=True, null=True)
    google_site_verification = models.CharField(_("Google Site Doğrulama"), max_length=255, blank=True, null=True)
    bing_site_verification = models.CharField(_("Bing Site Doğrulama"), max_length=255, blank=True, null=True)
    yandex_verification = models.CharField(_("Yandex Doğrulama"), max_length=255, blank=True, null=True)
    
    # Sosyal Medya OG Bilgileri
    og_image = models.ImageField(_("Sosyal Medya Paylaşım Görseli"), upload_to="general/", blank=True, null=True,
                               help_text=_("Sosyal medyada paylaşıldığında görünecek görsel. (1200x630px önerilir)"))
    og_type = models.CharField(_("OG Türü"), max_length=50, default="website")
    og_locale = models.CharField(_("OG Dil"), max_length=10, default="tr_TR")
    
    # Yerel İş Bilgileri (Local Business)
    business_type = models.CharField(_("İşletme Türü"), max_length=100, default="LegalService", 
                                   help_text=_("Schema.org işletme türü, varsayılan: LegalService"))
    business_founded = models.CharField(_("Kuruluş Yılı"), max_length=4, blank=True, null=True)
    business_location_lat = models.CharField(_("Enlem"), max_length=20, blank=True, null=True)
    business_location_long = models.CharField(_("Boylam"), max_length=20, blank=True, null=True)
    business_opening_hours = models.TextField(_("Çalışma Saatleri"), blank=True, null=True,
                                            help_text=_("Örnek: Mo-Fr 09:00-18:00"))
    
    class Meta:
        verbose_name = _("Site Ayarları")
        verbose_name_plural = _("Site Ayarları")
    
    def __str__(self):
        return self.site_name


class Page(models.Model):
    """Sabit sayfalar modeli"""
    title = models.CharField(_("Başlık"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    content = HTMLField(_("İçerik"))
    meta_title = models.CharField(_("Meta Başlık"), max_length=200, blank=True, null=True)
    meta_description = models.TextField(_("Meta Açıklama"), blank=True, null=True)
    meta_keywords = models.TextField(_("Meta Anahtar Kelimeler"), blank=True, null=True,
                                   help_text=_("Virgülle ayrılmış anahtar kelimeler."))
    is_active = models.BooleanField(_("Aktif"), default=True)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    
    class Meta:
        verbose_name = _("Sayfa")
        verbose_name_plural = _("Sayfalar")
    
    def __str__(self):
        return self.title


class SEOMetaData(models.Model):
    """Hukuk bürosu için özel SEO meta verileri"""
    title = models.CharField(_("Başlık"), max_length=100,
                           help_text=_("Bu meta veri kümesinin adı (yönetim için)"))
    target_url = models.CharField(_("Hedef URL"), max_length=255, unique=True,
                                help_text=_("Bu meta verilerin uygulanacağı URL (örn: /hizmetler/icra-hukuku/)"))
    meta_title = models.CharField(_("Meta Başlık"), max_length=200)
    meta_description = models.TextField(_("Meta Açıklama"), 
                                      help_text=_("160 karakteri geçmemelidir."))
    meta_keywords = models.TextField(_("Meta Anahtar Kelimeler"),
                                   help_text=_("Virgülle ayrılmış anahtar kelimeler."))
    og_title = models.CharField(_("OG Başlık"), max_length=200, blank=True, null=True)
    og_description = models.TextField(_("OG Açıklama"), blank=True, null=True)
    og_image = models.ImageField(_("OG Görsel"), upload_to="seo/", blank=True, null=True)
    is_active = models.BooleanField(_("Aktif"), default=True)
    canonical_url = models.URLField(_("Canonical URL"), blank=True, null=True,
                                  help_text=_("Yinelenen içerik için canonical URL belirtin (gerekirse)."))
    is_noindex = models.BooleanField(_("No Index"), default=False,
                                   help_text=_("Bu sayfa arama motorları tarafından indekslenmemeli mi?"))
    is_nofollow = models.BooleanField(_("No Follow"), default=False,
                                    help_text=_("Bu sayfadaki bağlantılar takip edilmemeli mi?"))
    schema_markup = models.TextField(_("Schema.org Markup"), blank=True, null=True,
                                   help_text=_("Sayfa için özel JSON-LD schema markup."))
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    
    class Meta:
        verbose_name = _("SEO Meta Verisi")
        verbose_name_plural = _("SEO Meta Verileri")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
