from django.urls import path

from .views import ordered_items_by_time_in_days, product_orders, product_full, get_clients, client_full, get_products

urlpatterns = [
    path('client/<int:client_id>/ordered_products/', ordered_items_by_time_in_days,
             name='ordered_products'),
    path('client/<int:client_id>/ordered_products/days/<int:days>/', ordered_items_by_time_in_days,
         name='ordered_products'),
    path('orders/product/<int:product_id>', product_orders, name='product_orders'),
    path('orders/product/<int:product_id>/days/<int:days>/', product_orders, name='product_orders_days'),
    path('products/', get_products, name='get_products'),
    path('product/<int:product_id>', product_full, name='product_full'),
    path('clients/', get_clients, name='get_clients'),
    path('clients/<int:client_id>/', client_full, name='client_full'),

]
