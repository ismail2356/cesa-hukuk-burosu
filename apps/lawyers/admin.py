from django.contrib import admin
from .models import Lawyer, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ['full_name_with_title', 'position', 'gender', 'is_active']
    list_filter = ['gender', 'is_active', 'position']
    search_fields = ['first_name', 'last_name', 'position']
    filter_horizontal = ['specializations']
    
    fields = (
        'title', 'first_name', 'last_name', 'gender', 'position',
        'photo', 'short_bio', 'email', 'phone',
        'specializations', 'expertise_areas',
        'education', 'experience', 'languages',
        'linkedin', 'twitter', 'order', 'is_active'
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = f"{obj.first_name.lower()}-{obj.last_name.lower()}"
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('specializations')
    
    def gender_display(self, obj):
        if obj.gender == 'M':
            return format_html('<span style="color: blue;">👨 Erkek</span>')
        else:
            return format_html('<span style="color: purple;">👩 Kadın</span>')
    gender_display.short_description = 'Cinsiyet'
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        count = queryset.update(is_active=True)
        messages.success(request, f'{count} avukat aktif yapıldı.')
    make_active.short_description = "✅ Seçili avukatları aktif yap"
    
    def make_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        messages.success(request, f'{count} avukat pasif yapıldı.')
    make_inactive.short_description = "❌ Seçili avukatları pasif yap"
