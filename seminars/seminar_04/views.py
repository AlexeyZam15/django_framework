from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404

from .forms import GamesForm, AuthorForm, ArticleForm, ClientForm, ProductForm, OrderForm, OrderedProductForm

import logging

from seminar_02.models import Author, Article, Comment

from homework_02.models import Client, Product, Order, OrderedProduct

logger = logging.getLogger(__name__)

"""
Задание №2
Доработаем задачу 1.
Создайте представление, которое выводит форму выбора.
В зависимости от переданных значений представление
вызывает одно из трёх представлений, созданных на
прошлом семинаре (если данные прошли проверку, конечно же).
"""


def games_choose(request):
    if request.method == 'POST':
        form = GamesForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data['game']
            attempts = form.cleaned_data['attempts']
            logger.info(f'Выбрана игра "{game}", с количеством попыток: {attempts}.')
            return redirect(game, attempts)
    else:
        form = GamesForm()
    context = {'title': 'Выбор игры',
               'form': form,
               }
    return render(request, 'seminar_04/games.html', context)


def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            logger.info(f'Создан автор: {author}.')
            return redirect('author_full', author.id)
    else:
        form = AuthorForm()
    context = {'title': 'Создание автора',
               'form': form,
               'action': 'Создать'
               }
    return render(request, 'seminar_04/form_create.html', context)


def author_update(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    form = AuthorForm(request.POST or None, instance=author)
    if request.method == 'POST':
        if form.is_valid():
            author = form.save()
            logger.info(f'Обновлен автор: {author}.')
            return redirect('author_full', author.id)
    context = {'title': 'Обновление автора',
               'form': form,
               'action': 'Изменить',
               }
    return render(request, 'seminar_04/form_create.html', context)


"""
Задание №4
Аналогично автору создайте форму добавления новой
статьи.
Автор статьи должен выбираться из списка (все доступные в
базе данных авторы).
"""


def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            logger.info(f'Создана статья: {article}.')
            return redirect('article_full', article.id)
    else:
        form = ArticleForm()
    context = {'title': 'Создание статьи',
               'form': form,
               'action': 'Создать',
               }
    return render(request, 'seminar_04/form_create.html', context)


def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    form = ArticleForm(request.POST or None, instance=article)
    if request.method == 'POST':
        if form.is_valid():
            article = form.save()
            logger.info(f'Обновлена статья: {article}.')
            return redirect('article_full', article.id)
    context = {'title': 'Обновление статьи',
               'form': form,
               'action': 'Изменить',
               }
    return render(request, 'seminar_04/form_create.html', context)


"""
Задание №5
Доработаем задачу 6 из прошлого семинара.
Мы сделали вывод статьи и комментариев.
Добавьте форму ввода нового комментария в
существующий шаблон.
"""

"""
Представления для форм клиентов, заказов и товаров
"""


def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            logger.info(f'Создан клиент: {client}.')
            return redirect('client_full', client.id)
    else:
        form = ClientForm()
    context = {'title': 'Создание клиента',
               'form': form,
               'action': 'Создать',
               }
    return render(request, 'seminar_04/orders_base_form_create.html', context)


def client_update(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST':
        if form.is_valid():
            client = form.save()
            logger.info(f'Обновлен клиент: {client}.')
            return redirect('client_full', client.id)
    context = {'title': 'Обновление клиента',
               'form': form,
               'action': 'Изменить',
               }
    return render(request, 'seminar_04/orders_base_form_create.html', context)


def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            product_photo = form.cleaned_data['photo']
            fs = FileSystemStorage()
            fs.save(product_photo.name, product_photo)
            product.photo = product_photo
            logger.info(f'Создан товар: {product}.')
            return redirect('product_full', product.id)
    context = {'title': 'Создание товара',
               'form': form,
               'action': 'Создать',
               }
    return render(request, 'seminar_04/orders_base_form_create.html', context)


def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            product_photo = form.cleaned_data['photo']
            fs = FileSystemStorage()
            fs.save(product_photo.name, product_photo)
            product.photo = product_photo
            logger.info(f'Обновлен товар: {product}.')
            return redirect('product_full', product.id)
    context = {'title': 'Обновление товара',
               'form': form,
               'action': 'Изменить',
               }
    return render(request, 'seminar_04/orders_base_form_create.html', context)


def order_create(request):
    form = OrderForm(request.POST or None)
    ordered_products = OrderedProduct.get_none_ordered_products()
    context = {'title': 'Создание заказа',
               'form': form,
               'action': 'Сделать заказ',
               'ordered_products': ordered_products,
               }
    if request.method == 'POST':
        if form.is_valid():
            client = form.cleaned_data['client']
            try:
                order = Order.create_order(client, ordered_products)
            except ValueError as ve:
                messages.error(request, ve)
                logger.error(f'{ve}')
                return redirect('order_create')
            logger.info(f'Создан заказ: {order}.')
            messages.success(request, f'Заказ {order.id} успешно создан')
            return redirect('order_full', order.id)
    return render(request, 'seminar_04/orders_order_form_create.html', context)


def order_create_product_add(request):
    form = OrderedProductForm(request.POST or None)
    context = {'title': 'Добавить товар к заказу',
               'form': form,
               'action': 'Добавить',
               }
    if request.method == 'POST':
        if form.is_valid():
            product_name = form.cleaned_data['product'].name
            product_count = form.cleaned_data['count']
            try:
                order = OrderedProduct.create_ordered_product(product_name, product_count)
                order.save()
            except ValueError as ve:
                messages.error(request, ve)
                logger.error(f'{ve}')
                return redirect('order_create_product_add')
            logger.info(f'В корзину добавлен товар {product_name} в количестве {product_count}.')
            return redirect('order_create')
    return render(request, 'seminar_04/orders_base_form_create.html', context)


def order_create_all_products_delete(request):
    OrderedProduct.cancel_ordered_products()
    logger.info(f'Корзина товаров очищена.')
    messages.success(request, f'Корзина товаров очищена')
    return redirect('order_create')


def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    logger.info(f'Удален заказ: {order_id}.')
    messages.success(request, f'Заказ {order_id} успешно удален')
    return redirect('get_orders')


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client_name = client.name
    client.delete()
    logger.info(f'Удален клиент: {client_name}.')
    messages.success(request, f'Клиент {client_name} успешно удален')
    return redirect('get_clients')


def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.name
    product.delete()
    logger.info(f'Удален товар: {product_name}.')
    messages.success(request, f'Товар {product_name} успешно удален')
    return redirect('get_products')
