from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Category, Tag, Article, Comment


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
        
        # Onaylı yorumları ekle
        context['comments'] = self.object.comments.filter(is_approved=True)
        
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


class CommentCreateView(View):
    """Yorum ekleme görünümü"""
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, status='published')
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        if name and email and content:
            Comment.objects.create(
                article=article,
                name=name,
                email=email,
                content=content
            )
            messages.success(request, 'Yorumunuz başarıyla gönderildi. Onaylandıktan sonra yayınlanacaktır.')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
        
        return redirect('blog:article_detail', slug=slug)
