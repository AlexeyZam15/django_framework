from django.db import models
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
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Приведение даты к временной зоне пользователя и нужному формату
        format_date = self.reg_date.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return (f'name: {self.name} email: {self.email} phone: {self.phone} address: {self.address} '
                f'reg_date: {format_date}')

    @property
    def orders(self):
        orders = Order.objects.filter(client=self).all()
        return orders


class Product(models.Model):
    """
    Поля модели «Товар»:
    — название товара
    — описание товара
    — цена товара
    — количество товара
    — дата добавления товара
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)
    photo = models.FileField(upload_to='photos', blank=True)

    def __str__(self):
        format_date = self.date_added.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return f'name: {self.name} description: {self.description} price: {self.price} ' \
               f'count: {self.count} date_added: {format_date}'

    @property
    def orders(self):
        orders = Order.objects.filter(ordered_products__product=self).all()
        return orders


class OrderedProduct(models.Model):
    """
    Поля модели «Заказанный товар»:
    — ссылка на товар
    — количество заказанного товара
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f'product: {self.product.name} count: {self.count}'

    # При создании объекта отнимать у продукта количество
    def save(self, *args, **kwargs):
        self.product.count -= self.count
        self.product.save()
        super().save(*args, **kwargs)


class Order(models.Model):
    """
    Поля модели «Заказ»:
    — связь с моделью «Клиент», указывает на клиента, сделавшего заказ
    — связь с моделью «Товар», указывает на товары, входящие в заказ
    — общая сумма заказа
    — дата оформления заказа
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ordered_products = models.ManyToManyField(OrderedProduct)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        format_date = self.order_date.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return (f'id: {self.pk} client: {self.client.name} products: '
                f'{", ".join([or_product.product.name + f" in count {or_product.count}" for or_product in self.ordered_products.all()])} total_price: {self.total_price} order date: '
                f'{format_date}')

    @staticmethod
    def create_order(client, products, date=None):
        ordered_products = []
        total_price = 0
        for product_name, product_count in products:
            product = Product.objects.filter(name=product_name).first()
            if product is None:
                raise ValueError(f'Product {product_name} not found')
            product_count = int(product_count)
            if product_count <= 0:
                raise ValueError(f'Count for ordered product must be greater than 0')
            while product.count < product_count:
                raise ValueError(
                    f'Not enough products in stock for {product_name}, ordered count = {product_count}')
            ordered_products.append(OrderedProduct.objects.create(
                product=product,
                count=product_count,
            ))
            total_price += product.price * product_count
            if not ordered_products:
                raise ValueError('No products in the order')
        order = Order.objects.create(
            client=client,
            total_price=total_price,
            order_date=date
        )
        order.ordered_products.set(ordered_products)
        return order

    def products_print(self):
        return ', '.join(
            [or_product.product.name + f"({or_product.count})" for or_product in self.ordered_products.all()])

    @property
    def get_ordered_products(self):
        return self.ordered_products.all()

    def save(self, *args, **kwargs):
        if not self.id:
            self.order_date = now()
        super().save(*args, **kwargs)
