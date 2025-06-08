from django.contrib import admin
from .models import Lawyer, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ['full_name_with_title', 'position', 'gender', 'is_active', 'order', 'created_at']
    list_filter = ['gender', 'is_active', 'specializations', 'created_at']
    search_fields = ['first_name', 'last_name', 'title', 'position']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    filter_horizontal = ['specializations']
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'first_name', 'last_name', 'slug', 'gender', 'photo', 'short_bio')
        }),
        ('İletişim Bilgileri', {
            'fields': ('email', 'phone')
        }),
        ('Profesyonel Bilgiler', {
            'fields': ('position', 'specializations', 'education', 'experience', 'expertise_areas', 'languages')
        }),
        ('Sosyal Medya', {
            'fields': ('linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Sistem Ayarları', {
            'fields': ('order', 'is_active'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('specializations')
