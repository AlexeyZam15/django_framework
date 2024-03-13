from django.shortcuts import render, get_object_or_404

from datetime import timedelta, datetime

"""
Для подготовки к 4 семинару
Измените шаблон для вывода заголовка и текста статьи, а также всех комментариев к статье с указанием текста комментария, 
автора комментария и даты обновления комментария в хронологическом порядке.

Если комментарий изменялся, дополнительно напишите “изменено”.
Не забывайте про представление с запросом в БД и маршруты. Проверьте, что они работают верно

сделано в seminar_03

Доработать магазин
Создайте шаблон для вывода всех заказов клиента и списком товаров внутри каждого заказа.
Подготовьте необходимый маршрут и представление.

сделано в seminar_03

Домашнее задание
Продолжаем работать с товарами и заказами.

Создайте шаблон, который выводит список заказанных клиентом товаров из всех его заказов с сортировкой по времени:
— за последние 7 дней (неделю)
— за последние 30 дней (месяц)
— за последние 365 дней (год)

Товары в списке не должны повторятся.
"""

from homework_02.models import Client, Product, Order


class ClientProduct:
    def __init__(self, product, count, date, total_price):
        self.product = product
        self.count = count
        self.date = date
        self.total_price = total_price


def ordered_items_by_time_in_days(request, client_id, days=None):
    client = Client.objects.get(id=client_id)
    client_orders = client.orders.all()
    if days:
        client_orders = client_orders.filter(order_date__gte=datetime.now() - timedelta(days=days)).all()
    # Объединить записи с одинаковыми именами, в дате оставить ближайшее к сегодняшней дате значение,
    # количество товара суммировать
    ordered_products_dict = {}
    for order in client_orders:
        for ordered_product in order.ordered_products.all():
            if ordered_product.product.name in ordered_products_dict:
                ordered_products_dict[ordered_product.product.name]['count'] += ordered_product.count
                ordered_products_dict[ordered_product.product.name][
                    'total_price'] += ordered_product.product.price * ordered_product.count
                if order.order_date > ordered_products_dict[ordered_product.product.name]['date']:
                    ordered_products_dict[ordered_product.product.name]['date'] = order.order_date
                continue
            ordered_products_dict[ordered_product.product.name] = {
                'product': ordered_product.product,
                'count': ordered_products_dict.get(ordered_product.product.name, {}).get('count',
                                                                                         0) + ordered_product.count,
                'date': order.order_date,
                'total_price': ordered_product.product.price * ordered_product.count,
            }
    client_products = [ClientProduct(**value) for value in sorted(ordered_products_dict.values(),
                                                                  key=lambda x: x['date'], reverse=True)]
    if days:
        # Определение окончания для слова день
        divided_days = days % 10
        if divided_days == 1:
            days_word = 'день'
        elif divided_days == 2 or divided_days == 3 or divided_days == 4:
            days_word = 'дня'
        else:
            days_word = 'дней'
        title = f'Заказанные товары за последние {days} {days_word} клиентом {client.name}'
    context = {
        'title': f'Все заказанные товары клиентом {client.name}',
        'columns': ['Название', 'Количество', 'Итоговая стоимость', 'Дата последнего заказа'],
        'client_products': client_products,
        'client_id': client_id,
    }
    return render(request, 'homework_03/client_products.html', context)


def product_orders(request, product_id, days=None):
    product = Product.objects.get(id=product_id)
    products = Order.objects.filter(ordered_products__product=product).all()
    if days:
        products = products.filter(order_date__gte=datetime.now() - timedelta(days=days)).all()
    context = {
        'title': f'Заказы с товаром {product.name}',
        'columns': ['id', 'Клиент', 'Заказанные продукты', 'Общая стоимость', 'Дата'],
        'orders': products,
        'product_id': product_id,
    }
    return render(request, 'homework_03/product_orders.html', context)


def product_full(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'title': f'Товар {product.name}',
        'product': product,
    }
    return render(request, 'homework_03/product.html', context)


def client_full(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    context = {
        'title': f'Клиент {client.name}',
        'client': client,
    }
    return render(request, 'homework_03/client.html', context)


def get_clients(request):
    clients = Client.objects.order_by('-reg_date').all()
    context = {
        'title': 'Клиенты',
        'columns': ['Имя', 'Почта', 'Телефон', 'Адрес', 'Дата регистрации'],
        'clients': clients,
    }
    return render(request, 'homework_03/clients.html', context)


def get_products(request):
    products = Product.objects.order_by('-date_added').all()
    context = {
        'title': 'Товары',
        'columns': ['Название', 'Описание', 'Цена', 'Количество', 'Дата добавления'],
        'products': products,
    }
    return render(request, 'homework_03/products.html', context)


def order_full(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'title': f'Заказ {order.id}',
        'order': order,
    }
    return render(request, 'homework_03/order.html', context)


def index(request):
    return render(request, 'homework_03/index.html')
