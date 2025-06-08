from django.contrib import admin
from .models import Lawyer


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ('full_name_with_title', 'position', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'position', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'position')
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}
    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': (
                ('title', 'first_name', 'last_name'),
                'slug',
                'gender',
                'photo',
                ('email', 'phone'),
                'position',
            )
        }),
        ('Detaylı Bilgiler', {
            'fields': (
                'education',
                'experience',
                'expertise_areas',
                'languages',
            ),
            'classes': ('collapse',),
        }),
        ('Sosyal Medya', {
            'fields': (
                'linkedin',
                'twitter',
            ),
            'classes': ('collapse',),
        }),
        ('Ayarlar', {
            'fields': (
                'order',
                'is_active',
            )
        }),
    )
