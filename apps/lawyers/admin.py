from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import Lawyer, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Uzmanlık Alanı Bilgileri', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Ayarlar', {
            'fields': ('is_active',)
        })
    )


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ['full_name_with_title', 'position', 'gender_display', 'photo_preview', 'is_active', 'order']
    list_filter = ['gender', 'is_active', 'position', 'created_at']
    search_fields = ['first_name', 'last_name', 'title', 'position']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    filter_horizontal = ['specializations']
    list_editable = ['order', 'is_active']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('👤 Kişisel Bilgiler', {
            'fields': ('title', 'first_name', 'last_name', 'slug', 'gender'),
            'description': 'Avukatın temel kişisel bilgileri'
        }),
        ('📷 Fotoğraf', {
            'fields': ('photo',),
            'description': 'Avukat fotoğrafını yükleyin (JPG, PNG formatında, max 5MB)'
        }),
        ('💼 Profesyonel Bilgiler', {
            'fields': ('position', 'short_bio'),
            'description': 'Pozisyon ve kısa biyografi bilgileri'
        }),
        ('📞 İletişim Bilgileri', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('🎓 Uzmanlık Alanları', {
            'fields': ('specializations', 'expertise_areas'),
            'description': 'Uzmanlık alanlarını seçin veya ek alanlar yazın'
        }),
        ('📚 Detaylı Bilgiler', {
            'fields': ('education', 'experience', 'languages'),
            'classes': ('collapse',)
        }),
        ('🌐 Sosyal Medya', {
            'fields': ('linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('⚙️ Sistem Ayarları', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius: 50%; object-fit: cover; border: 2px solid #ddd;" />',
                obj.photo.url
            )
        return format_html('<span style="color: #999;">📷 Fotoğraf Yok</span>')
    photo_preview.short_description = 'Fotoğraf'
    
    def gender_display(self, obj):
        if obj.gender == 'M':
            return format_html('<span style="color: blue;">👨 Erkek</span>')
        else:
            return format_html('<span style="color: purple;">👩 Kadın</span>')
    gender_display.short_description = 'Cinsiyet'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('specializations')
    
    def save_model(self, request, obj, form, change):
        # Eğer slug boşsa otomatik oluştur
        if not obj.slug:
            obj.slug = f"{obj.first_name.lower()}-{obj.last_name.lower()}"
        
        super().save_model(request, obj, form, change)
        
        if change:
            messages.success(request, f'{obj.full_name_with_title()} bilgileri güncellendi.')
        else:
            messages.success(request, f'{obj.full_name_with_title()} sisteme eklendi.')
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        count = queryset.update(is_active=True)
        messages.success(request, f'{count} avukat aktif yapıldı.')
    make_active.short_description = "✅ Seçili avukatları aktif yap"
    
    def make_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        messages.success(request, f'{count} avukat pasif yapıldı.')
    make_inactive.short_description = "❌ Seçili avukatları pasif yap"
