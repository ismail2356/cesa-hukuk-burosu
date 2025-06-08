from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField


class Category(models.Model):
    """Makale kategorisi modeli"""
    name = models.CharField('Kategori Adı', max_length=100)
    slug = models.SlugField('URL', max_length=120, unique=True, blank=True)
    description = models.TextField('Açıklama', blank=True, null=True)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Makale etiketi modeli"""
    name = models.CharField('Etiket Adı', max_length=50)
    slug = models.SlugField('URL', max_length=60, unique=True, blank=True)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Etiket'
        verbose_name_plural = 'Etiketler'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Makale modeli"""
    STATUS_CHOICES = (
        ('draft', 'Taslak'),
        ('published', 'Yayınlandı'),
    )
    
    title = models.CharField('Başlık', max_length=200)
    slug = models.SlugField('URL', max_length=220, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='Yazar')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name='Kategori')
    tags = models.ManyToManyField(Tag, related_name='articles', verbose_name='Etiketler', blank=True)
    image = models.ImageField('Kapak Görseli', upload_to='articles/', blank=True, null=True)
    summary = models.TextField('Özet', blank=True, null=True)
    content = HTMLField('İçerik')
    status = models.CharField('Durum', max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField('Öne Çıkan', default=False)
    view_count = models.PositiveIntegerField('Görüntülenme Sayısı', default=0)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)
    published_at = models.DateTimeField('Yayınlanma Tarihi', blank=True, null=True)

    class Meta:
        verbose_name = 'Makale'
        verbose_name_plural = 'Makaleler'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Status published olduğunda published_at otomatik ayarla
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status == 'draft':
            self.published_at = None
            
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Makale yorumu modeli"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Makale')
    name = models.CharField('Ad Soyad', max_length=100)
    email = models.EmailField('E-posta')
    content = models.TextField('Yorum')
    is_approved = models.BooleanField('Onaylı', default=False)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.article.title}"
