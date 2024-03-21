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
    list_display = ('name', 'description', 'show_photo', 'price', 'count', 'date_added')
    search_fields = ('name', 'description', 'price', 'count', 'date_added')
    list_per_page = 15
    ordering = ('-date_added',)
    readonly_fields = ['show_photo', 'date_added']

    @admin.display(description='Фото')
    def show_photo(self, product: Product):
        if product.photo:
            return mark_safe(f'<img src="{product.photo.url}" width="100">')
        return 'Фото отсутствует'


admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderedProduct, OrderedProductAdmin)
admin.site.register(Order, OrderAdmin)
