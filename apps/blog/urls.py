from django.urls import path
from .views import (
    article_list, 
    article_detail, 
    category_detail, 
    tag_detail
)

app_name = 'blog'

urlpatterns = [
    path('', article_list, name='article_list'),
    path('makale/<slug:slug>/', article_detail, name='article_detail'),
    path('kategori/<slug:slug>/', category_detail, name='category_detail'),
    path('etiket/<slug:slug>/', tag_detail, name='tag_detail'),
] 