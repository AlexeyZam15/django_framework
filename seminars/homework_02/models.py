from django.contrib import admin, messages
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

"""
Создайте три модели Django: клиент, товар и заказ.

Клиент может иметь несколько заказов. Заказ может содержать несколько товаров. Товар может входить в несколько заказов.

*Допишите несколько функций CRUD для работы с моделями по желанию. Что по вашему мнению актуально в такой базе данных.
"""


class Client(models.Model):
    """
    Поля модели «Клиент»:
    — имя клиента
    — электронная почта клиента
    — номер телефона клиента
    — адрес клиента
    — дата регистрации клиента
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='имя')
    email = models.EmailField(verbose_name='электронная почта')
    phone = models.CharField(max_length=20, verbose_name='номер телефона')
    address = models.CharField(max_length=100, verbose_name='адрес')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')
    change_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    def __str__(self):
        # Приведение даты к временной зоне пользователя и нужному формату
        format_date = self.reg_date.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return (f'name: {self.name} email: {self.email} phone: {self.phone} address: {self.address} '
                f'reg_date: {format_date} change_date: {self.change_date}')

    @property
    def orders(self):
        orders = Order.objects.filter(client=self).all()
        return orders

    def get_absolute_url(self):
        return reverse('client_full', kwargs={'client_id': self.pk})

    class Meta:
        ordering = ['-change_date']
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Product(models.Model):
    """
    Поля модели «Товар»:
    — название товара
    — описание товара
    — цена товара
    — количество товара
    — дата добавления товара
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='название')
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    count = models.IntegerField(verbose_name='количество', default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True, verbose_name='дата добавления')
    photo = models.FileField(upload_to='photos', blank=True, null=True, verbose_name='фото')

    def __str__(self):
        format_date = self.date_added.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return f'name: {self.name} description: {self.description} price: {self.price} ' \
               f'count: {self.count} date_added: {format_date}'

    @property
    def orders(self):
        orders = Order.objects.filter(ordered_products__product=self).all()
        return orders

    def get_absolute_url(self):
        return reverse('product_full', kwargs={'product_id': self.pk})

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class OrderedProduct(models.Model):
    """
    Поля модели «Заказанный товар»:
    — ссылка на товар
    — количество заказанного товара
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    count = models.IntegerField(verbose_name='количество', default=0, blank=True, null=True)
    in_order = models.ForeignKey('Order', on_delete=models.CASCADE, default=None, null=True, blank=True,
                                 verbose_name='в заказе')
    date_added = models.DateTimeField(auto_now=True, verbose_name='дата добавления')

    def __str__(self):
        return f'product: {self.product.name} count: {self.count} order: {self.in_order}'

    @staticmethod
    def create_ordered_product(product_name: str, ordered_count: int):
        product = Product.objects.filter(name=product_name).first()
        if product is None:
            raise ValueError(f'Product {product_name} not found')
        if ordered_count <= 0:
            raise ValueError(f'Count for ordered product must be greater than 0')
        while product.count < ordered_count:
            raise ValueError(
                f'Not enough products in stock for {product_name} in count {ordered_count}')
        return OrderedProduct(
            product=product,
            count=ordered_count,
        )

    def save(self, *args, **kwargs):
        if self.in_order is None:
            self.product.count -= self.count
            self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.in_order is None:
            self.product.count += self.count
            self.product.save()
        super().delete(*args, **kwargs)

    @staticmethod
    def cancel_ordered_products():
        for or_product in OrderedProduct.objects.filter(in_order=None):
            or_product.delete()

    @staticmethod
    def get_none_ordered_products():
        return OrderedProduct.objects.filter(in_order=None).all()

    class Meta:
        ordering = ['-product__date_added']
        verbose_name = 'заказанный товар'
        verbose_name_plural = 'заказанные товары'

    @admin.display(description="Товар")
    def product_name(self):
        return self.product.name

    @admin.display(description="Заказ")
    def order_id(self):
        return self.in_order.pk if self.in_order else 'в корзине'


class Order(models.Model):
    """
    Поля модели «Заказ»:
    — связь с моделью «Клиент», указывает на клиента, сделавшего заказ
    — связь с моделью «Товар», указывает на товары, входящие в заказ
    — общая сумма заказа
    — дата оформления заказа
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    ordered_products = models.ManyToManyField(OrderedProduct, verbose_name='заказанные товары')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='общая сумма')
    order_date = models.DateTimeField(auto_now=True, verbose_name='дата заказа')

    def __str__(self):
        format_date = self.order_date.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return (f'id: {self.pk} client: {self.client.name} products: '
                f'{", ".join([or_product.product.name + f" in count {or_product.count}" for or_product in self.ordered_products.all()])} total_price: {self.total_price} order date: '
                f'{format_date}')

    @staticmethod
    def create_order(client, ordered_products, date=None):
        order = Order(
            client=client,
            order_date=date,
        )
        if not ordered_products:
            raise ValueError('No products in the order')
        order.save()
        order.set_ordered_products(ordered_products)
        order.set_total_price()
        order.save()
        return order

    def products_print(self):
        return ', '.join(
            [or_product.product.name + f"({or_product.count})" for or_product in self.ordered_products.all()])

    def set_total_price(self):
        self.total_price = sum(
            or_product.product.price * or_product.count for or_product in self.ordered_products.all())

    def set_ordered_products(self, ordered_products):
        self.ordered_products.set(ordered_products)
        for or_product in filter(lambda x: x.in_order is None, ordered_products):
            or_product.in_order = self
            or_product.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order_date = now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('order_full', kwargs={'order_id': self.pk})

    def get_ordered_products(self):
        return self.ordered_products.all()

    class Meta:
        ordering = ['-order_date']
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    @admin.display(description='Заказанные товары')
    def display_ordered_products(self):
        return self.products_print()

    @admin.display(description='Клиент')
    def client_name(self):
        return self.client.name
