from django.contrib import admin, messages

import logging

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
from homework_02.models import Client, Product, Order, OrderedProduct
from seminar_04.forms import OrderForm, OrderedProductForm

logger = logging.getLogger(__name__)


class OrderAdmin(admin.ModelAdmin):
    # form = OrderForm
    list_display = ('id', 'client_name', 'display_ordered_products', 'total_price', 'order_date')
    search_fields = ('client__name', 'ordered_products__product__name',)
    readonly_fields = ['total_price', 'order_date']
    filter_horizontal = ('ordered_products',)
    list_per_page = 15
    ordering = ('-order_date',)
    autocomplete_fields = ['client']
    actions = ['cancel_order']
    list_filter = ('client__name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        filter_qs = OrderedProduct.objects.filter(in_order=None) | (OrderedProduct.objects.filter(in_order=obj))
        form.base_fields['ordered_products'].queryset = filter_qs
        return form

    def save_model(self, request, obj, form, change):
        client = form.cleaned_data['client']
        ordered_products = form.cleaned_data['ordered_products']
        if obj is None:
            obj.create_order(client, ordered_products)
        else:
            obj.client = form.cleaned_data['client']
            obj.save()
            obj.set_ordered_products(ordered_products)
            obj.set_total_price()
        return super().save_model(request, obj, form, change)


class OrderedProductAdmin(admin.ModelAdmin):
    form = OrderedProductForm
    list_display = ('id', 'product_name', 'count', 'order_id', 'date_added')
    search_fields = ('product__name', 'in_order__client__name', 'in_order__id')
    readonly_fields = ['in_order']
    list_per_page = 15
    ordering = ('-date_added',)
    list_filter = ('product__name',)
    autocomplete_fields = ['product']

    actions = ['cancel_ordered_products']

    @admin.action(description="Отменить товары в корзине")
    def cancel_ordered_products(self, request, queryset):
        ordered_products = queryset.filter(in_order=None)
        if not ordered_products:
            messages.error(request, "Выберите товары в корзине")
            logger.error("Товары в корзине не выбраны")
            return
        for or_product in ordered_products:
            or_product.delete()
            logger.info(f"Товар {or_product.product.name} удалён из корзины")
        messages.success(request, "Выбранные товары в корзине отменены")

    def save_model(self, request, obj, form, change):
        product_name = form.cleaned_data['product'].name
        count = form.cleaned_data['count']
        obj.create_ordered_product(product_name, count)
        return super().save_model(request, obj, form, change)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'reg_date', 'change_date')
    search_fields = ('name', 'email', 'phone', 'address', 'reg_date', 'change_date')
    list_per_page = 15
    ordering = ('-change_date',)
    readonly_fields = ['reg_date', 'change_date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'count', 'date_added')
    search_fields = ('name', 'description', 'price', 'count', 'date_added')
    list_per_page = 15
    ordering = ('-date_added',)
    readonly_fields = ['date_added']


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
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderedProduct, OrderedProductAdmin)
admin.site.register(Order, OrderAdmin)
