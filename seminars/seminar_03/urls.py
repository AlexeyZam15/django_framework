from django.urls import path

from .views import index, about, coin, dice, random_number, article_full, get_articles, article_comments, get_orders, get_authors

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('coin/<int:count>/', coin, name='coin'),
    path('dice/<int:count>/', dice, name='dice'),
    path('random_number/<int:max_n>/<int:count>', random_number, name='rnd'),
    path('articles/', get_articles, name='get_articles'),
    path('articles/author/<int:author_id>/', get_articles, name='author_articles'),
    path('articles/<int:article_id>/', article_full, name='article_full'),
    path('articles/<int:article_id>/comments/', article_comments, name='article_comments'),
    path('orders/', get_orders, name='get_orders'),
    path('authors/', get_authors, name='get_authors'),
]
