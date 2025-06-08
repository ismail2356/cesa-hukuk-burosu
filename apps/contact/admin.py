from django.contrib import admin
from .models import ContactMessage, OfficeLocation


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Seçili mesajları okundu olarak işaretle"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Seçili mesajları okunmadı olarak işaretle"


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_main', 'is_active', 'order')
    list_filter = ('is_main', 'is_active')
    search_fields = ('name', 'address', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'address', 'phone', 'email')
        }),
        ('Harita', {
            'fields': ('google_maps_link', 'google_maps_embed')
        }),
        ('Ayarlar', {
            'fields': ('is_main', 'is_active', 'order')
        }),
        ('Zaman Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
