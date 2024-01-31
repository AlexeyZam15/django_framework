import random

from django.db import models

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
    side = models.CharField(unique=True, max_length=1, choices=CHOICES)
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
