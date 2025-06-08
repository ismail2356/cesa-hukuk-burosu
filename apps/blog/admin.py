from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Ayarlar', {
            'fields': ('is_active',)
        })
    )
    
    def article_count(self, obj):
        return obj.articles.filter(status='published').count()
    article_count.short_description = 'Makale Sayısı'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug')
        }),
        ('Ayarlar', {
            'fields': ('is_active',)
        })
    )
    
    def article_count(self, obj):
        return obj.articles.filter(status='published').count()
    article_count.short_description = 'Makale Sayısı'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'featured', 'image_preview', 'view_count', 'published_at']
    list_filter = ['status', 'featured', 'category', 'author', 'created_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['view_count', 'published_at', 'created_at', 'updated_at', 'slug']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'featured']
    list_per_page = 20
    
    fieldsets = (
        ('📝 Makale Bilgileri', {
            'fields': ('title', 'slug', 'author'),
            'description': 'Başlık yazıldığında URL otomatik oluşturulur'
        }),
        ('🏷️ Kategori ve Etiketler', {
            'fields': ('category', 'tags'),
            'description': 'Makaleyi kategorilere ayırın ve etiketleyin'
        }),
        ('🖼️ Kapak Görseli', {
            'fields': ('image',),
            'description': 'Makale için kapak görseli yükleyin. Önerilen boyut: 1200x630px'
        }),
        ('📄 İçerik', {
            'fields': ('summary', 'content'),
            'description': 'Özet alanı SEO için çok önemlidir'
        }),
        ('⚙️ Yayın Ayarları', {
            'fields': ('status', 'featured'),
            'description': 'Durumu "Yayınlandı" seçtiğinizde makale sitede görünür olacak'
        }),
        ('📊 İstatistikler', {
            'fields': ('view_count', 'published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 6px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">📷 Görsel Yok</span>')
    image_preview.short_description = 'Kapak Görseli'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('tags')
    
    def save_model(self, request, obj, form, change):
        # Eğer yazar atanmamışsa, mevcut kullanıcıyı ata
        if not obj.author:
            obj.author = request.user
        
        # Status published olduğunda published_at otomatik ayarla
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
            messages.success(request, f'"{obj.title}" makalesi başarıyla yayınlandı!')
        elif obj.status == 'draft':
            obj.published_at = None
            
        super().save_model(request, obj, form, change)
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    def make_published(self, request, queryset):
        count = 0
        for article in queryset:
            if article.status != 'published':
                article.status = 'published'
                if not article.published_at:
                    article.published_at = timezone.now()
                article.save()
                count += 1
        messages.success(request, f'{count} makale yayınlandı.')
    make_published.short_description = "✅ Seçili makaleleri yayınla"
    
    def make_draft(self, request, queryset):
        count = queryset.update(status='draft', published_at=None)
        messages.success(request, f'{count} makale taslak yapıldı.')
    make_draft.short_description = "📝 Seçili makaleleri taslak yap"
    
    def make_featured(self, request, queryset):
        count = queryset.update(featured=True)
        messages.success(request, f'{count} makale öne çıkarıldı.')
    make_featured.short_description = "⭐ Seçili makaleleri öne çıkar"
    
    def remove_featured(self, request, queryset):
        count = queryset.update(featured=False)
        messages.success(request, f'{count} makalenin öne çıkarma durumu kaldırıldı.')
    remove_featured.short_description = "❌ Öne çıkarma durumunu kaldır"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'article', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content', 'article__title']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_approved']
    list_per_page = 25
    
    fieldsets = (
        ('👤 Yorum Sahibi', {
            'fields': ('name', 'email')
        }),
        ('📝 Yorum İçeriği', {
            'fields': ('article', 'content')
        }),
        ('✅ Onay Durumu', {
            'fields': ('is_approved',)
        }),
        ('📅 Tarihler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'İçerik Önizleme'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article')
    
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        messages.success(request, f'{count} yorum onaylandı.')
    approve_comments.short_description = "✅ Seçili yorumları onayla"
    
    def reject_comments(self, request, queryset):
        count = queryset.update(is_approved=False)
        messages.success(request, f'{count} yorum reddedildi.')
    reject_comments.short_description = "❌ Seçili yorumları reddet"
