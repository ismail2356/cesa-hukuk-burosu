from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, Page, SEOMetaData


# User modelini özelleştirelim
class CustomUserAdmin(UserAdmin):
    """Özelleştirilmiş kullanıcı admin paneli"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Kişisel Bilgiler'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('İzinler'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        (_('Önemli Tarihler'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('İzinler'), {
            'fields': ('is_staff', 'is_superuser', 'groups'),
        }),
    )
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Seçili kullanıcıları aktif yap"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Seçili kullanıcıları pasif yap"


# Group admin panelini de özelleştirelim
class CustomGroupAdmin(admin.ModelAdmin):
    """Özelleştirilmiş kullanıcı grupları admin paneli"""
    list_display = ('name', 'get_users_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = 'Kullanıcı Sayısı'


# Varsayılan admin panellerini kaldırıp, özelleştirilmiş panelleri kaydedelim
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Site ayarları admin paneli yapılandırması"""
    fieldsets = (
        (_("Genel Bilgiler"), {
            "fields": ("site_name", "logo", "favicon")
        }),
        (_("İletişim Bilgileri"), {
            "fields": ("email", "phone", "address", "whatsapp")
        }),
        (_("Sosyal Medya"), {
            "fields": ("facebook", "instagram", "linkedin", "twitter")
        }),
        (_("SEO - Temel"), {
            "fields": ("meta_title", "meta_description", "meta_keywords", "meta_author", "meta_copyright"),
        }),
        (_("SEO - Doğrulama ve Analitik"), {
            "fields": ("google_analytics", "google_site_verification", "bing_site_verification", "yandex_verification"),
            "classes": ("collapse",),
        }),
        (_("SEO - Sosyal Medya"), {
            "fields": ("og_image", "og_type", "og_locale"),
            "classes": ("collapse",),
        }),
        (_("SEO - Yerel İşletme"), {
            "fields": ("business_type", "business_founded", "business_location_lat", 
                      "business_location_long", "business_opening_hours"),
            "classes": ("collapse",),
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir tane site ayarları kaydı olabilir
        return SiteSettings.objects.count() == 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Sayfalar admin paneli yapılandırması"""
    list_display = ("title", "slug", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (_("Sayfa Bilgileri"), {
            "fields": ("title", "slug", "content", "is_active")
        }),
        (_("SEO"), {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
            "classes": ("collapse",)
        }),
    )


@admin.register(SEOMetaData)
class SEOMetaDataAdmin(admin.ModelAdmin):
    """SEO Meta Verileri admin paneli yapılandırması"""
    list_display = ("title", "target_url", "is_active", "is_noindex", "updated_at")
    list_filter = ("is_active", "is_noindex", "is_nofollow")
    search_fields = ("title", "target_url", "meta_keywords", "meta_description")
    fieldsets = (
        (_("Temel Bilgiler"), {
            "fields": ("title", "target_url", "is_active")
        }),
        (_("Meta Etiketleri"), {
            "fields": ("meta_title", "meta_description", "meta_keywords")
        }),
        (_("OpenGraph"), {
            "fields": ("og_title", "og_description", "og_image"),
            "classes": ("collapse",)
        }),
        (_("İleri SEO Ayarları"), {
            "fields": ("canonical_url", "is_noindex", "is_nofollow"),
            "classes": ("collapse",)
        }),
        (_("Schema.org"), {
            "fields": ("schema_markup",),
            "classes": ("collapse",)
        }),
    )
