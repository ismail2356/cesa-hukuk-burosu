from django.contrib import admin
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'featured', 'published_at', 'view_count']
    list_filter = ['status', 'featured', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['view_count', 'published_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'image')
        }),
        ('İçerik', {
            'fields': ('summary', 'content')
        }),
        ('Yayın Ayarları', {
            'fields': ('status', 'featured', 'published_at')
        }),
        ('İstatistikler', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('tags')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'article', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content', 'article__title']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article')
