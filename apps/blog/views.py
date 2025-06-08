from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Category, Tag, Article


def article_list(request):
    """Blog ana sayfa - sadece yayınlanmış makaleler"""
    articles = Article.objects.filter(
        status='published',
        published_at__isnull=False
    ).select_related('author', 'category').prefetch_related('tags').order_by('-published_at')
    
    # Arama
    search_query = request.GET.get('q')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Kategori filtresi
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        articles = articles.filter(category=selected_category)
    
    # Tag filtresi
    tag_slug = request.GET.get('tag')
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug, is_active=True)
        articles = articles.filter(tags=selected_tag)
    
    # Sayfalama
    paginator = Paginator(articles, 9)  # Sayfa başına 9 makale
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Öne çıkan makaleler (sadece ana sayfada göster)
    featured_articles = []
    if not search_query and not category_slug and not tag_slug:
        featured_articles = Article.objects.filter(
            status='published',
            featured=True,
            published_at__isnull=False
        ).select_related('author', 'category')[:3]
    
    # Kategoriler ve taglar
    categories = Category.objects.filter(is_active=True).order_by('name')
    tags = Tag.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'featured_articles': featured_articles,
        'categories': categories,
        'tags': tags,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
        'search_query': search_query,
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    """Makale detay sayfası"""
    article = get_object_or_404(
        Article.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status='published',
        published_at__isnull=False
    )
    
    # Görüntülenme sayısını artır
    article.view_count += 1
    article.save(update_fields=['view_count'])
    
    # İlgili makaleler (aynı kategoriden)
    related_articles = Article.objects.filter(
        category=article.category,
        status='published',
        published_at__isnull=False
    ).exclude(id=article.id).order_by('-published_at')[:4]
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'blog/article_detail.html', context)


def category_detail(request, slug):
    """Kategori detay sayfası"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    articles = Article.objects.filter(
        category=category,
        status='published',
        published_at__isnull=False
    ).select_related('author', 'category').order_by('-published_at')
    
    # Sayfalama
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, slug):
    """Tag detay sayfası"""
    tag = get_object_or_404(Tag, slug=slug, is_active=True)
    
    articles = Article.objects.filter(
        tags=tag,
        status='published',
        published_at__isnull=False
    ).select_related('author', 'category').order_by('-published_at')
    
    # Sayfalama
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_detail.html', context)


class ArticleListView(ListView):
    """Makale listesi görünümü"""
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        """Sadece yayınlanmış makaleleri listele"""
        return Article.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['tags'] = Tag.objects.filter(is_active=True)
        context['featured_articles'] = Article.objects.filter(
            status='published', 
            featured=True
        )[:5]
        return context


class ArticleDetailView(DetailView):
    """Makale detay görünümü"""
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    
    def get_queryset(self):
        """Sadece yayınlanmış makaleleri göster"""
        return Article.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Görüntülenme sayısını artır
        self.object.view_count += 1
        self.object.save()
        
        # İlgili makaleleri ekle
        context['related_articles'] = Article.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id)[:4]
        
        return context


class CategoryArticleListView(ListView):
    """Kategori bazlı makale listesi görünümü"""
    model = Article
    template_name = 'blog/category_article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        """Belirli bir kategorideki yayınlanmış makaleleri listele"""
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Article.objects.filter(category=self.category, status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagArticleListView(ListView):
    """Etiket bazlı makale listesi görünümü"""
    model = Article
    template_name = 'blog/tag_article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        """Belirli bir etikete sahip yayınlanmış makaleleri listele"""
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'], is_active=True)
        return Article.objects.filter(tags=self.tag, status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchArticleListView(ListView):
    """Arama sonuçları görünümü"""
    model = Article
    template_name = 'blog/search_article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        """Arama sorgusuna göre makaleleri filtrele"""
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) | 
                Q(content__icontains=query),
                status='published'
            )
        return Article.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
