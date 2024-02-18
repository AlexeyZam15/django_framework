import random

from django.contrib import admin
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
        (HEADS, 'Орёл'),
        (TAILS, 'Решка'),
    )
    choices = [HEADS, TAILS]
    side = models.CharField(max_length=1, choices=CHOICES, verbose_name='Сторона')
    time = models.DateTimeField(auto_now=True, verbose_name='Время броска')

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

    class Meta:
        ordering = ['-time']
        verbose_name = 'Монета'
        verbose_name_plural = 'Монеты'

    @admin.display(description='Сторона')
    def get_side(self):
        return 'Решка' if self.side == 'T' else 'Орёл'

    def throw(self):
        """Бросок монеты"""
        self.side = random.choice(self.choices)
        self.save()
        return self.side


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
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    bio = models.TextField(verbose_name='Биография', null=True, blank=True)
    birth_date = models.DateField(verbose_name='День рождения', null=True, blank=True)
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    change_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

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

    @property
    def articles(self):
        return Article.objects.filter(author=self)

    class Meta:
        ordering = ['-change_date']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


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
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(max_length=100, verbose_name='Категория')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    change_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

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

    @property
    def comments(self):
        return Comment.objects.filter(article=self).all()

    def __str__(self):
        formatted_date = self.date_published.strftime('%d.%m.%Y %H:%M:%S')
        return f"{self.title} {self.content} {formatted_date} {self.author.full_name} {self.category} {self.views} {self.is_published}"

    class Meta:
        ordering = ['-change_date']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    @admin.display(description="Автор")
    def author_full_name(self):
        return self.author.full_name


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
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

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

    def is_changed(self):
        """Сравнение даты создания и изменения без учёта секунд"""
        return self.date_created.strftime('%d.%m.%Y %H:%M') != self.date_modified.strftime('%d.%m.%Y %H:%M')

    class Meta:
        ordering = ['-date_modified']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    @admin.display(description='Автор')
    def author_full_name(self):
        return self.author.full_name

    @admin.display(description='Статья')
    def article_title(self):
        return self.article.title
