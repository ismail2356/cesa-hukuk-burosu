from django.urls import path
from .views import (
    ArticleListView, 
    ArticleDetailView, 
    CategoryArticleListView, 
    TagArticleListView, 
    SearchArticleListView,
    CommentCreateView
)

app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('makale/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('kategori/<slug:slug>/', CategoryArticleListView.as_view(), name='category_article_list'),
    path('etiket/<slug:slug>/', TagArticleListView.as_view(), name='tag_article_list'),
    path('arama/', SearchArticleListView.as_view(), name='search_article_list'),
    path('makale/<slug:slug>/yorum/', CommentCreateView.as_view(), name='comment_create'),
] 