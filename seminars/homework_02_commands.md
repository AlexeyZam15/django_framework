# Клиент

## Создание

```commandline
python manage.py create_client client1 client1@mail.ru phone1 address1
python manage.py create_client client2 client2@mail.ru phone2 address2
python manage.py create_client client3 client3@mail.ru phone3 address3
python manage.py create_client client4 client4@mail.ru phone4 address4
```

## Обновление

```commandline
python manage.py update_client client1 -n newclient1 -e newclient1@mail.ru -p newphone1 -a newaddress1
```

## Удаление

```commandline
python manage.py delete_client client3
```

## Чтение

```commandline
python manage.py get_clients
python manage.py get_clients -c 1
python manage.py get_clients -f name__startswith c
```

# Товар

## Создание

```commandline
python manage.py create_product product1 desc1 101 1
python manage.py create_product product2 desc2 202 2
python manage.py create_product product3 desc3 303 3
python manage.py create_product product4 desc4 404 4
```

## Обновление

```commandline
python manage.py update_product product1 -n product99 -d desc99 -p 99.99 -c 99
```

## Удаление

```commandline
python manage.py delete_product product4
```

## Чтение

```commandline
python manage.py get_products
python manage.py get_products -c 1
python manage.py get_products -f price__gt 100
```

# Заказ

## Создание

```commandline
python manage.py create_order newclient1 -p product2 1 -p product99 10
python manage.py create_order client2 -p product2 1 -p product99 10
python manage.py create_order client4 -p product99 10
python manage.py create_order client4 -p product3 4
```

## Удаление

python manage.py delete_order <order_id>

## Чтение

```commandline
python manage.py get_orders
python manage.py get_orders -c 1
python manage.py get_orders -f client__name newclient1
python manage.py get_orders -p name product2
```

# Чистка базы данных

```commandline
python manage.py delete_all_clients
python manage.py delete_all_products
```

Если отдельно удалять только таблицу с заказами

```commandline
python manage.py delete_all_orders
```

