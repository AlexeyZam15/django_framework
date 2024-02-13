from dateutil.utils import today
from django import forms
from django.db.transaction import commit
from django.shortcuts import get_object_or_404
from seminar_02.models import Author, Article, Comment
from homework_02.models import Client, Product, Order, OrderedProduct

"""
# Задание №1
Доработаем задачу про броски монеты, игральной кости и
случайного числа.
Создайте форму, которая предлагает выбрать: монета, кости,
числа.
Второе поле предлагает указать количество попыток от 1 до 64.
"""


class GamesForm(forms.Form):
    game = forms.ChoiceField(
        choices=[('coin', 'Монета'), ('dice', 'Кость'), ('random_number', 'Случайное число')],
        label='Выберите игру')
    attempts = forms.IntegerField(label='Количество попыток')


"""
Задание №3
Продолжаем работу с авторами, статьями и комментариями.
Создайте форму для добавления нового автора в базу данных.
Используйте ранее созданную модель Author
"""


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'email', 'bio', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-group'}),
            'last_name': forms.TextInput(attrs={'class': 'form-group'}),
            'email': forms.EmailInput(attrs={'class': 'form-group'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'bio': 'Биография',
            'birth_date': 'Дата рождения',
        }


#
# class AuthorForm(forms.Form):
#     first_name = forms.CharField(label='Имя',
#                                  widget=forms.TextInput(attrs={'class': 'form-group'}))
#     last_name = forms.CharField(label='Фамилия',
#                                 widget=forms.TextInput(attrs={'class': 'form-group'}))
#     email = forms.EmailField(label='Email',
#                              widget=forms.EmailInput(attrs={'class': 'form-group'}))
#
#     bio = forms.CharField(label='Биография',
#                           widget=forms.Textarea(attrs={'class': 'form-control'}))
#     birth_date = forms.DateField(label='Дата рождения',
#                                  widget=forms.DateInput(attrs={'class': 'form-control',
#                                                                'type': 'date'}))
#
#     def save(self):
#         author = Author(
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name'],
#             email=self.cleaned_data['email'],
#             bio=self.cleaned_data['bio'],
#             birth_date=self.cleaned_data['birth_date'].strftime('%d.%m.%Y'),
#         )
#         author.save()
#         return author


"""
Задание №4
Аналогично автору создайте форму добавления новой
статьи.
Автор статьи должен выбираться из списка (все доступные в
базе данных авторы).
"""


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-group'}),
            'category': forms.TextInput(attrs={'class': 'form-group'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-group'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст',
            'author': 'Автор',
            'category': 'Категория',
            'is_published': 'Опубликовано',
        }


# class ArticleForm(forms.Form):
#     title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control'}))
#     author = forms.ModelChoiceField(queryset=Author.objects.all(),
#                                     label='Автор', widget=forms.Select(attrs={'class': 'form-control'}))
#     category = forms.CharField(label='Категория', widget=forms.TextInput(attrs={'class': 'form-group'}))
#     is_published = forms.BooleanField(label='Опубликовано', required=False,
#                                       widget=forms.CheckboxInput(attrs={'class': 'form-group'}))
#
#     def save(self):
#         article = Article(
#             title=self.cleaned_data['title'],
#             content=self.cleaned_data['content'],
#             author=self.cleaned_data['author'],
#             category=self.cleaned_data['category'],
#             is_published=self.cleaned_data['is_published'],
#         )
#         article.save()
#         return article


"""
Задание №5
Доработаем задачу 6 из прошлого семинара.
Мы сделали вывод статьи и комментариев.
Добавьте форму ввода нового комментария в
существующий шаблон.
"""


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'comment']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-group'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'author': 'Автор',
            'comment': 'Текст',
        }


# class CommentForm(forms.Form):
#     author = forms.ModelChoiceField(queryset=Author.objects.all(),
#                                     label='Автор', widget=forms.Select(attrs={'class': 'form-control'}))
#     comment = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control'}))
#
#     def save(self, article):
#         comment = Comment(
#             author=self.cleaned_data['author'],
#             comment=self.cleaned_data['comment'],
#             article=article,
#         )
#         comment.save()
#         return comment


"""
Формы для создание клиентов, заказов и товаров из прошлого семинара.
"""


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-group'}),
            'email': forms.EmailInput(attrs={'class': 'form-group'}),
            'phone': forms.TextInput(attrs={'class': 'form-group'}),
            'address': forms.TextInput(attrs={'class': 'form-group'}),
        }
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес',
        }


# class ClientForm(forms.Form):
#     name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-group'}))
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-group'}))
#     phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-group'}))
#     address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'class': 'form-group'}))
#
#     def save(self):
#         client = Client(
#             name=self.cleaned_data['name'],
#             email=self.cleaned_data['email'],
#             phone=self.cleaned_data['phone'],
#             address=self.cleaned_data['address'],
#         )
#         client.save()
#         return client


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'count', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-group'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-group'}),
            'count': forms.NumberInput(attrs={'class': 'form-group'}),
            'photo': forms.FileInput(attrs={'class': 'form-group'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'count': 'Количество',
            'photo': 'Фото',
        }


# class ProductForm(forms.Form):
#     name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     price = forms.DecimalField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     count = forms.IntegerField(label='Количество', widget=forms.NumberInput(attrs={'class': 'form-control'}))
#
#     def save(self):
#         product = Product(
#             name=self.cleaned_data['name'],
#             price=self.cleaned_data['price'],
#             count=self.cleaned_data['count'],
#         )
#         product.save()
#         return product

class OrderedProductForm(forms.ModelForm):
    class Meta:
        model = OrderedProduct
        fields = ['product', 'count']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-group'}),
            'count': forms.NumberInput(attrs={'class': 'form-group'}),
        }
        labels = {
            'product': 'Товар',
            'count': 'Количество',
        }


# class OrderedProductForm(forms.Form):
#     product = forms.ModelChoiceField(queryset=Product.objects.all(),
#                                      label='Товар', widget=forms.Select(attrs={'class': 'form-group'}))
#     count = forms.IntegerField(label='Количество', widget=forms.NumberInput(attrs={'class': 'form-group'}))
#
#     def save(self):
#         ordered_product = OrderedProduct(
#             product=self.cleaned_data['product'],
#             count=self.cleaned_data['count'],
#         )
#         ordered_product.save()
#         return ordered_product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-group'}),
        }
        labels = {
            'client': 'Клиент',
        }
