from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class ServiceCategory(models.Model):
    """Hizmet kategorisi modeli"""
    name = models.CharField('Kategori Adı', max_length=100)
    slug = models.SlugField('URL', max_length=120, unique=True, blank=True)
    description = models.TextField('Açıklama', blank=True, null=True)
    icon = models.CharField('İkon', max_length=50, blank=True, null=True, 
                           help_text='Font Awesome ikon kodu (örn: fa-balance-scale)')
    meta_title = models.CharField('Meta Başlık', max_length=200, blank=True, null=True,
                                help_text='SEO için özel başlık (boş bırakılırsa kategori adı kullanılır)')
    meta_description = models.TextField('Meta Açıklama', blank=True, null=True,
                                     help_text='SEO için özel açıklama (boş bırakılırsa kategori açıklaması kullanılır)')
    order = models.PositiveIntegerField('Sıralama', default=0)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Hizmet Kategorisi'
        verbose_name_plural = 'Hizmet Kategorileri'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Hizmet modeli"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, 
                                 related_name='services', verbose_name='Kategori')
    title = models.CharField('Başlık', max_length=200)
    slug = models.SlugField('URL', max_length=220, unique=True, blank=True)
    short_description = models.TextField('Kısa Açıklama', blank=True, null=True)
    content = HTMLField('İçerik')
    image = models.ImageField('Görsel', upload_to='services/', blank=True, null=True)
    icon = models.CharField('İkon', max_length=50, blank=True, null=True,
                           help_text='Font Awesome ikon kodu (örn: fa-gavel)')
    meta_title = models.CharField('Meta Başlık', max_length=200, blank=True, null=True,
                                help_text='SEO için özel başlık (boş bırakılırsa hizmet başlığı kullanılır)')
    meta_description = models.TextField('Meta Açıklama', blank=True, null=True,
                                     help_text='SEO için özel açıklama (boş bırakılırsa kısa açıklama kullanılır)')
    is_featured = models.BooleanField('Öne Çıkan', default=False)
    order = models.PositiveIntegerField('Sıralama', default=0)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'
        ordering = ['category', 'order', 'title']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
