import logging

from django.http import HttpResponse
from django.utils import lorem_ipsum

logger = logging.getLogger(__name__)


def index(request):
    html = """
    <html>
        <head>
            <title>Главная</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """
    logger.info("переход на главную страницу")
    return HttpResponse(html)


def about(request):
    html = f"""
    <html>
        <head>
            <title>О нас</title>
        </head>
        <body>
            <h1>О нас</h1>
            <p>{lorem_ipsum.sentence()}</p>
        </body>
    </html>
    """
    logger.info("переход на страницу 'О нас'")
    return HttpResponse(html)
