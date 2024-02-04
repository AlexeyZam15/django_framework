from django.db import models

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
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        format_date = self.date_added.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        return f'name: {self.name} description: {self.description} price: {self.price} ' \
               f'count: {self.count} date_added: {format_date}'


class OrderedProduct(models.Model):
    """
    Поля модели «Заказанный товар»:
    — ссылка на товар
    — количество заказанного товара
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f'product: {self.product.name} count: {self.count}'


class Order(models.Model):
    """
    Поля модели «Заказ»:
    — связь с моделью «Клиент», указывает на клиента, сделавшего заказ
    — связь с моделью «Товар», указывает на товары, входящие в заказ
    — общая сумма заказа
    — дата оформления заказа
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through=OrderedProduct)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f'id: {self.pk} client: {self.client.name} products: '
                f'{", ".join([product.name + f" in count {product.orderedproduct_set.filter(order=self).first().count}" for product in self.products.all()])} total_price: {self.total_price} order date: '
                f'{self.order_date}')
