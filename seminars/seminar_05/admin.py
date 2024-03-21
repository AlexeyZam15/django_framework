from django.contrib import admin, messages

import logging

from django.utils.safestring import mark_safe

# Register your models here.

"""
Задание №2
Подключите к админ панели созданные вами в рамках
прошлых семинаров модели в приложениях:
○ броски монеты,
○ блог,
○ магазин,
○ другие, если вы их создавали.
"""

from seminar_02.models import Coin
from seminar_02.models import Author, Article, Comment

logger = logging.getLogger(__name__)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'bio', 'birth_date', 'reg_date', 'change_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_per_page = 15
    ordering = ('-change_date',)
    readonly_fields = ['reg_date', 'change_date']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_full_name', 'article_title', 'date_created', 'date_modified')
    search_fields = (
        'author__first_name', 'author__last_name', 'article__title', 'comment', 'date_created', 'date_modified')
    list_per_page = 15
    ordering = ('-date_modified',)
    readonly_fields = ['date_created', 'date_modified']
    list_filter = ('article', 'author')
    autocomplete_fields = ['author', 'article']


class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_side', 'time')
    search_fields = ('side',)
    list_per_page = 15
    ordering = ('-time',)
    readonly_fields = ['time']
    list_filter = ('side',)
    actions = ['throw_coins']

    @admin.action(description="Перебросить монеты")
    def throw_coins(self, request, queryset):
        coins = queryset
        if not coins:
            messages.error(request, "Выберите монеты, которые хотите перебросить")
            logger.error("Монеты не выбраны")
            return
        for coin in coins:
            coin.throw()
            logger.info(f"Монета {coin.id} переброшена, результат: {coin.get_side()}")
        messages.success(request, "Выбранные монеты переброшены")

    def get_search_results(self, request, queryset, search_term):
        if search_term == "Орёл":
            search_term = "H"
        elif search_term == "Решка":
            search_term = "T"
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author_full_name', 'category', 'views', 'is_published', 'date_published', 'change_date')
    search_fields = ('title', 'author__first_name', 'author__last_name', 'category')
    list_per_page = 15
    ordering = ('-change_date',)
    readonly_fields = ['date_published', 'change_date']
    list_filter = ('author', 'is_published', 'category')
    autocomplete_fields = ['author']
    actions = ['publish_articles', 'hide_articles']
    list_display_links = ('id', 'title')

    @admin.action(description="Опубликовать статьи")
    def publish_articles(self, request, queryset):
        articles = queryset.filter(is_published=False)
        if not articles:
            messages.error(request, "Выберите скрытые статьи, которые хотите опубликовать")
            logger.error("Скрытые статьи не выбраны")
            return
        for article in articles:
            article.is_published = True
            article.save()
            logger.info(f"Статья {article.id} опубликована")
        messages.success(request, "Выбранные статьи опубликованы")

    @admin.action(description="Скрыть статьи")
    def hide_articles(self, request, queryset):
        articles = queryset.filter(is_published=True)
        if not articles:
            messages.error(request, "Выберите статьи, которые хотите скрыть")
            logger.error("Опубликованные статьи не выбраны")
            return
        for article in articles:
            article.is_published = False
            article.save()
            logger.info(f"Статья {article.id} скрыта")
        messages.success(request, "Выбранные статьи скрыты")


admin.site.register(Coin, CoinAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
