from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def article_count(self, obj):
        return obj.articles.filter(status='published').count()
    article_count.short_description = 'Makale Sayısı'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def article_count(self, obj):
        return obj.articles.filter(status='published').count()
    article_count.short_description = 'Makale Sayısı'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'featured', 'image_thumbnail', 'view_count', 'published_at']
    list_filter = ['status', 'featured', 'category', 'author', 'created_at', 'published_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['view_count', 'published_at', 'created_at', 'updated_at']
    date_hierarchy = 'published_at'
    list_editable = ['status', 'featured']
    list_per_page = 20
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Kapak Görseli', {
            'fields': ('image',),
            'description': 'Makale için kapak görseli yükleyin (JPG, PNG formatında, önerilen boyut: 1200x630px)'
        }),
        ('İçerik', {
            'fields': ('summary', 'content'),
            'description': 'Özet alanı SEO için önemlidir, 150-160 karakter arası olmalı'
        }),
        ('Yayın Ayarları', {
            'fields': ('status', 'featured'),
            'description': 'Durumu "Yayınlandı" seçtiğinizde makale otomatik olarak sitede görünür olacak'
        }),
        ('İstatistikler', {
            'fields': ('view_count', 'published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "Görsel Yok"
    image_thumbnail.short_description = 'Kapak Görseli'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('tags')
    
    def save_model(self, request, obj, form, change):
        # Eğer yazar atanmamışsa, mevcut kullanıcıyı ata
        if not obj.author_id:
            obj.author = request.user
        
        # Status published olduğunda published_at otomatik ayarla
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
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
        self.message_user(request, f'{count} makale yayınlandı.')
    make_published.short_description = "Seçili makaleleri yayınla"
    
    def make_draft(self, request, queryset):
        count = queryset.update(status='draft', published_at=None)
        self.message_user(request, f'{count} makale taslak yapıldı.')
    make_draft.short_description = "Seçili makaleleri taslak yap"
    
    def make_featured(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f'{count} makale öne çıkarıldı.')
    make_featured.short_description = "Seçili makaleleri öne çıkar"
    
    def remove_featured(self, request, queryset):
        count = queryset.update(featured=False)
        self.message_user(request, f'{count} makalenin öne çıkarma durumu kaldırıldı.')
    remove_featured.short_description = "Öne çıkarma durumunu kaldır"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'article', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content', 'article__title']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_approved']
    list_per_page = 25
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'İçerik Önizleme'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article')
    
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} yorum onaylandı.')
    approve_comments.short_description = "Seçili yorumları onayla"
    
    def reject_comments(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} yorum reddedildi.')
    reject_comments.short_description = "Seçili yorumları reddet"
