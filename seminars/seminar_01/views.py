import logging

from django.http import HttpResponse
from django.shortcuts import render
from random import randint


# Create your views here.

def index(request):
    return HttpResponse('Hello, World!')


"""
три простых представления,
возвращающих HTTP ответ:
- Орёл или решка
- Значение одной из шести граней игрального кубика
- Случайное число от 0 до 100
Добавьте логирование в проект.
"""

logger = logging.getLogger(__name__)


def coin(request):
    rnd = randint(0, 1)
    res = 'Орёл' if rnd else 'Решка'
    logger.info(f'На монете выпало: {res}')
    return HttpResponse(f'На монете выпало: {res}')


def dice(request):
    rnd = randint(1, 6)
    logger.info(f'На кубике выпало: {rnd}')
    return HttpResponse(f'На кубике выпало: {rnd}')


def random_hundred(request):
    rnd = randint(0, 100)
    logger.info(f'Случайное число от 0 до 100: {rnd}')
    return HttpResponse(f'Случайное число от 0 до 100: {rnd}')
