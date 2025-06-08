from django.contrib import admin
from django.utils.html import strip_tags
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Arama motorları için özel başlık ve açıklama'
        }),
        ('Ayarlar', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('category', 'title', 'slug', 'short_description', 'content')
        }),
        ('Medya', {
            'fields': ('image', 'icon')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Arama motorları için özel başlık ve açıklama'
        }),
        ('Ayarlar', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Short description alanındaki HTML etiketlerini temizle
        if obj.short_description:
            obj.short_description = strip_tags(obj.short_description)
        super().save_model(request, obj, form, change)
