from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os


def validate_image_size(image):
    """Resim boyutunu kontrol et (5MB limit)"""
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError('Resim boyutu 5MB\'dan küçük olmalıdır.')


def lawyer_photo_upload(instance, filename):
    """Avukat fotoğrafları için upload path"""
    ext = filename.split('.')[-1]
    filename = f"{instance.first_name}_{instance.last_name}.{ext}"
    return f'lawyers/{filename}'


class Specialization(models.Model):
    """Uzmanlık alanı modeli"""
    name = models.CharField('Uzmanlık Alanı', max_length=100)
    slug = models.SlugField('URL', max_length=120, unique=True, blank=True)
    description = models.TextField('Açıklama', blank=True, null=True)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Uzmanlık Alanı'
        verbose_name_plural = 'Uzmanlık Alanları'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Lawyer(models.Model):
    """Avukat modeli"""
    GENDER_CHOICES = (
        ('M', 'Erkek'),
        ('F', 'Kadın'),
    )
    
    title = models.CharField('Unvan', max_length=50, help_text='Örn: Av., Dr., Prof. Dr.')
    first_name = models.CharField('Ad', max_length=100)
    last_name = models.CharField('Soyad', max_length=100)
    slug = models.SlugField('URL', max_length=200, unique=True, blank=True)
    gender = models.CharField('Cinsiyet', max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(
        'Fotoğraf', 
        upload_to=lawyer_photo_upload, 
        blank=True, 
        null=True,
        validators=[validate_image_size],
        help_text='JPG, PNG formatında, maksimum 5MB'
    )
    short_bio = models.TextField('Kısa Biyografi', max_length=200, blank=True, null=True, help_text='Maksimum 200 karakter')
    email = models.EmailField('E-posta', blank=True, null=True)
    phone = models.CharField('Telefon', max_length=20, blank=True, null=True)
    position = models.CharField('Pozisyon', max_length=100, help_text='Örn: Kurucu Ortak, Kıdemli Avukat, Stajyer Avukat')
    specializations = models.ManyToManyField(Specialization, verbose_name='Uzmanlık Alanları', blank=True)
    education = models.TextField('Eğitim', blank=True, null=True)
    experience = models.TextField('Deneyim', blank=True, null=True)
    expertise_areas = models.TextField('Diğer Uzmanlık Alanları', blank=True, null=True, help_text='Yukarıdaki uzmanlık alanlarına ek olarak')
    languages = models.CharField('Yabancı Diller', max_length=200, blank=True, null=True)
    linkedin = models.URLField('LinkedIn', blank=True, null=True)
    twitter = models.URLField('Twitter', blank=True, null=True)
    order = models.PositiveIntegerField('Sıralama', default=0, help_text='Avukatların görüntülenme sırası (0=en üstte)')
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Avukat'
        verbose_name_plural = 'Avukatlar'
        ordering = ['order', 'last_name']

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_name_with_title(self):
        return f"{self.title} {self.first_name} {self.last_name}"
