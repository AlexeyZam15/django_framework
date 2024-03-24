"""
Задание №1
Изменяем задачу 8 из семинара 1 с выводом двух html страниц:
главной и о себе.
Перенесите вёрстку в шаблоны.
Представления должны пробрасывать полезную информацию в
шаблон через контекст.

Задание №2
Доработаем задачу 1.
Выделите общий код шаблонов и создайте родительский
шаблон base.html.
Внесите правки в дочерние шаблоны.


"""
from random import randint

from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import lorem_ipsum

from datetime import timedelta, datetime


def index(request):
    context = {
        'title': 'Главная страница',
        'content': 'Добро пожаловать на наш сайт!',
    }
    return render(request, 'seminar_03/page.html', context)


def about(request):
    context = {
        'title': 'О нас',
        'content': lorem_ipsum.paragraph(),
    }
    return render(request, 'seminar_03/page.html', context)


"""
Задание №3
Доработаем задачу 7 из урока 1, где бросали монетку,
игральную кость и генерировали случайное число.
Маршруты могут принимать целое число - количество
бросков.
Представления создают список с результатами бросков и
передают его в контекст шаблона.
Необходимо создать универсальный шаблон для вывода
результатов любого из трёх представлений.
"""

from pandas import DataFrame


def coin(request, count):
    res_list = []
    for i in range(1, count + 1):
        rnd = randint(0, 1)
        res = 'Орёл' if rnd else 'Решка'
        res_list.append((i, res,))
    table = DataFrame(res_list, columns=['Бросок', 'Результат'])
    context = {
        'title': 'Бросок монетки',
        'content': table.to_html(index=False),
    }
    return render(request, 'seminar_03/page.html', context)


def dice(request, count):
    res_list = []
    for i in range(1, count + 1):
        rnd = randint(1, 6)
        res_list.append((i, rnd,))
    table = DataFrame(res_list, columns=['Бросок', 'Результат'])
    context = {
        'title': 'Бросок костей',
        'content': table.to_html(index=False),
    }
    return render(request, 'seminar_03/page.html', context)


def random_number(request, max_n=100, count=1):
    res_list = [(i, randint(1, max_n)) for i in range(1, count + 1)]
    table = DataFrame(res_list, columns=['Бросок', 'Результат'])
    context = {
        'title': f'Бросок до {max_n}',
        'content': table.to_html(index=False),
    }
    return render(request, 'seminar_03/page.html', context)


"""
Задание №4
Доработаем задачи из прошлого семинара по созданию
моделей автора, статьи и комментария.
Создайте шаблон для вывода всех статей автора в виде
списка заголовков.
○ Если статья опубликована, заголовок должен быть
ссылкой на статью.
○ Если не опубликована, без ссылки.
Не забываем про код представления с запросом к базе
данных и маршруты.
"""

from seminar_02.models import Article, Author

from seminar_04.forms import CommentForm


def get_articles(request, author_id=None):
    articles = Article.objects.filter(is_published=True).order_by('-date_published').all()
    if author_id:
        author = get_object_or_404(Author, pk=author_id)
        articles = Article.objects.filter(author=author).all()
        title = f'Статьи автора {author.full_name}'
    else:
        title = 'Статьи'
    context = {
        'title': title,
        'columns': ['Заголовок', 'Дата публикации', 'Автор публикации', 'Категория', 'Просмотры', 'Опубликована',
                    'Комментариев'],
        'articles': articles,
    }
    return render(request, 'seminar_03/articles.html', context)


"""
Задание №5
Доработаем задачу 4.
Создай шаблон для вывода подробной информации о
статье.
Внесите изменения в views.py - создайте представление и в
urls.py - добавьте маршрут.
*Увеличивайте счётчик просмотра статьи на единицу при
каждом просмотре
"""


def article_full(request, article_id, comment_id=None):
    article = get_object_or_404(Article, pk=article_id)
    if comment_id:
        comment = get_object_or_404(Comment, pk=comment_id, article=article)
        form = CommentForm(request.POST or None, instance=comment)
        form_state = 'collapse show'
        action = 'Изменить'
    else:
        form = CommentForm(request.POST or None)
        form_state = 'collapse'
        action = 'Добавить'
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_full', article_id=article_id)
    else:
        article.views += 1
    comments = Comment.objects.order_by('-date_modified').filter(article=article).select_related('author').all()
    context = {'title': f'Статья автора {article.author.full_name} ', 'article': article, 'form': form,
               'comments': comments, 'form_state': form_state, 'action': action}
    return render(request, 'seminar_03/article.html', context)


"""
Задание №6
Измените шаблон для вывода заголовка и текста статьи, а
также всех комментариев к статье с указанием текста
комментария, автора комментария и даты обновления
комментария в хронологическом порядке.
Если комментарий изменялся, дополнительно напишите
“изменено”.
Не забывайте про представление с запросом в БД и
маршруты. Проверьте, что они работают верно
"""

from seminar_02.models import Comment


def article_comments(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment.objects.order_by('date_modified').filter(article=article).select_related('author').all()
    context = {
        'title': f'Комментарии к статье {article.title}',
        'columns': ['Комментарий', 'Дата создания', 'Дата изменения', 'Изменено'],
        'comments': comments,
    }
    return render(request, 'seminar_03/comments.html', context)


"""
Задание №7
Доработаем задачу 8 из прошлого семинара про клиентов,
товары и заказы.
Создайте шаблон для вывода всех заказов клиента и
списком товаров внутри каждого заказа.
Подготовьте необходимый маршрут и представление.
"""

from homework_02.models import Order, OrderedProduct, Product, Client


def get_orders(request, client_id=None, days=None):
    orders = Order.objects.all()
    title = 'Заказы'
    if client_id:
        client = get_object_or_404(Client, pk=client_id)
        orders = Order.objects.filter(client=client).all()
        title += f' клиента {client.name}'
    if days:
        orders = orders.filter(order_date__gte=datetime.now() - timedelta(days=days)).all()
        title += f' за последние {days} дней'
    context = {
        'title': title,
        'orders': orders.order_by('-order_date').all(),
        'columns': ['id', 'Клиент', 'Заказанные продукты', 'Общая стоимость', 'Дата'],
        'client_id': client_id,
    }
    return render(request, 'seminar_03/orders.html', context)


"""Представления для авторов"""


def get_authors(request):
    authors = Author.objects.order_by('-id').all()
    context = {
        'title': 'Авторы',
        'columns': ['Автор', 'Почта', 'Дата рождения', 'Статьи'],
        'authors': authors,
    }
    return render(request, 'seminar_03/authors.html', context)


def author_full(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {'title': f'Автор {author.full_name}', 'author': author}
    return render(request, 'seminar_03/author.html', context)
