from django.urls import path
from .views import games_choose, author_create, article_create, client_create, product_create, order_create, \
    author_update, article_update, client_update, product_update, order_create_product_add, order_delete, \
    product_delete, client_delete, order_create_all_products_delete
from homework_03.views import index
from seminar_03.views import article_full

urlpatterns = [
    path('games/', games_choose, name='games_choose'),
    path('authors/create/', author_create, name='author_create'),
    path('articles/create/', article_create, name='article_create'),
    path('clients/create/', client_create, name='client_create'),
    path('clients/<int:client_id>/update/', client_update, name='client_update'),
    path('clients/<int:client_id>/delete/', client_delete, name='client_delete'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:product_id>/update/', product_update, name='product_update'),
    path('products/<int:product_id>/delete/', product_delete, name='product_delete'),
    path('orders/create/', order_create, name='order_create'),
    path('orders/<int:order_id>/delete/', order_delete, name='order_delete'),
    path('orders/create/product_add/', order_create_product_add, name='order_create_product_add'),
    path('orders/create/products_delete/', order_create_all_products_delete, name='order_create_all_products_delete'),
    path('authors/<int:author_id>/update/', author_update, name='author_update'),
    path('articles/<int:article_id>/update/', article_update, name='article_update'),
    path('articles/<int:article_id>/comment/<int:comment_id>/update/', article_full, name='comment_update'),
    path('', index, name='index'),
]
