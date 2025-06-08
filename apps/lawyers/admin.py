from django.contrib import admin
from django.utils.html import format_html
from .models import Lawyer, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ['full_name_with_title', 'position', 'gender', 'photo_thumbnail', 'is_active', 'order']
    list_filter = ['gender', 'is_active', 'position', 'created_at']
    search_fields = ['first_name', 'last_name', 'title', 'position']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    filter_horizontal = ['specializations']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'first_name', 'last_name', 'slug', 'gender', 'position')
        }),
        ('Fotoğraf', {
            'fields': ('photo',),
            'description': 'Avukat fotoğrafını yükleyin (JPG, PNG formatında, max 5MB)'
        }),
        ('Biyografi', {
            'fields': ('short_bio',),
            'description': 'Kısa biyografi (maksimum 200 karakter)'
        }),
        ('İletişim Bilgileri', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Uzmanlık Alanları', {
            'fields': ('specializations', 'expertise_areas'),
            'description': 'Uzmanlık alanlarını seçin veya ek alanlar yazın'
        }),
        ('Detaylı Bilgiler', {
            'fields': ('education', 'experience', 'languages'),
            'classes': ('collapse',)
        }),
        ('Sosyal Medya', {
            'fields': ('linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Ayarlar', {
            'fields': ('order', 'is_active'),
        })
    )
    
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "Fotoğraf Yok"
    photo_thumbnail.short_description = 'Fotoğraf'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('specializations')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Eğer slug boşsa otomatik oluştur
        if not obj.slug:
            obj.slug = f"{obj.first_name.lower()}-{obj.last_name.lower()}"
            obj.save()
