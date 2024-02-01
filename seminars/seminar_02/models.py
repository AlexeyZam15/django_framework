import random

from django.db import models

from datetime import date

"""
Задание 1
Создайте модель для запоминания бросков монеты: орёл или
решка.
Также запоминайте время броска

Задание №2
Доработаем задачу 1.
Добавьте статический метод для статистики по n последним
броскам монеты.
Метод должен возвращать словарь с парой ключей значений, для орла и для решки.
"""


class Coin(models.Model):
    HEADS = 'H'
    TAILS = 'T'
    CHOICES = (
        (HEADS, 'Heads'),
        (TAILS, 'Tails'),
    )
    choices = [HEADS, TAILS]
    side = models.CharField(max_length=1, choices=CHOICES)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.side} {self.time}'

    @staticmethod
    def get_statistics(n):
        """Собирает значения сколько выпадал орёл или решка в последних n монетах"""""
        heads_count = 0
        tails_count = 0
        if n is None:
            coins = Coin.objects.all()
        else:
            coins = Coin.objects.order_by('-time')[:n]
        for coin in coins:
            if coin.side == Coin.HEADS:
                heads_count += 1
            else:
                tails_count += 1
        return {
            'Heads': heads_count,
            'Tails': tails_count,
        }

    @staticmethod
    def get_coins(n):
        """Возвращает n последних монет"""
        return Coin.objects.order_by('-time')[:n]


"""
Задание 3
Создайте модель Автор. Модель должна содержать
следующие поля:
○ имя до 100 символов
○ фамилия до 100 символов
○ почта
○ биография
○ день рождения
Дополнительно создай пользовательское поле “полное
имя”, которое возвращает имя и фамилию.
"""


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    birth_date = models.CharField(max_length=10)

    fields = ['first_name', 'last_name', 'email', 'bio', 'birth_date']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} {self.email} {self.bio} {self.birth_date}'

    """CRUD функции"""

    @staticmethod
    def create_author(first_name, last_name, email, bio, birth_date):
        return Author.objects.create(first_name=first_name, last_name=last_name, email=email, bio=bio,
                                     birth_date=birth_date)

    @staticmethod
    def get_authors():
        return Author.objects.all()

    @staticmethod
    def get_author(author_id):
        return Author.objects.filter(id=author_id).first()

    @staticmethod
    def update_author(author_id, attr, new_value):
        author = Author.get_author(author_id)
        if author is None:
            return None
        setattr(author, attr, new_value)
        author.save()

    @staticmethod
    def delete_author(author_id):
        author = Author.get_author(author_id)
        if author is None:
            return None
        author.delete()
        return author


"""
Задание 4
Создайте модель Статья (публикация). Авторы из прошлой задачи могут
писать статьи. У статьи может быть только один автор. У статьи должны быть
следующие обязательные поля:
○ заголовок статьи с максимальной длиной 200 символов
○ содержание статьи
○ дата публикации статьи
○ автор статьи с удалением связанных объектов при удалении автора
○ категория статьи с максимальной длиной 100 символов
○ количество просмотров статьи со значением по умолчанию 0
○ флаг, указывающий, опубликована ли статья со значением по умолчанию
False

Задача 5
Доработаем задачу 4.
Создай четыре функции для реализации CRUD в модели
Django Article (статья).
*Используйте Django команды для вызова функций.
"""


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)

    fields = ['title', 'content', 'category', 'views']

    @staticmethod
    def create_article(data):
        return Article.objects.create(**data)

    @staticmethod
    def get_articles():
        return Article.objects.all()

    @staticmethod
    def get_article(article_id):
        return Article.objects.filter(id=article_id).first()

    @staticmethod
    def update_article(article_id, field, value):
        article = Article.get_article(article_id)
        if article is None:
            return None
        setattr(article, field, value)
        article.save()
        return article

    @staticmethod
    def delete_article(article_id):
        article = Article.get_article(article_id)
        if article is None:
            return None
        article.delete()
        return article

    def __str__(self):
        formatted_date = self.date_published.strftime('%d.%m.%Y %H:%M:%S')
        return f"{self.title} {self.content} {formatted_date} {self.author.full_name} {self.category} {self.views} {self.is_published}"


"""
Задание №6
Создайте модель Комментарий.
Авторы могут добавлять комментарии к своим и чужим
статьям. Т.е. у комментария может быть один автор.
И комментарий относится к одной статье. У модели должны
быть следующие поля
○ автор
○ статья
○ комментарий
○ дата создания
○ дата изменения

Задание №7
Создайте функции для работы с базой данных:
○ Поиск всех статей автора по его имени
○ Поиск всех комментариев автора по его имени
○ Поиск всех комментариев по названию статьи
Каждая из трёх функций должна иметь возможность
сортировки и ограничение выборки по количеству.
"""


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    fields = ['comment']

    def __str__(self):
        format_date_create = self.date_created.strftime('%d.%m.%Y %H:%M:%S')
        format_date_mod = self.date_modified.strftime('%d.%m.%Y %H:%M:%S')
        return f"{self.author.full_name} {self.article.title} {self.comment} {format_date_create} {format_date_mod}"

    @staticmethod
    def get_comments(count=None, args=None, values=None):
        if args is not None and values is not None:
            data = Comment.objects.filter(args, values).all()
        else:
            data = Comment.objects.all()
        if count is not None:
            data = data[:count]
        return data
