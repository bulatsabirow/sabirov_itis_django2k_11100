from django.db import models


class StatusEnum(models.TextChoices):
    in_warehouse = 'in warehouse', 'На складе'
    in_transit = 'in transit', 'В пути'
    delivery_point = 'delivery point', 'В пункте выдачи'
    delivered = 'delivered', 'Доставлен'


class Role(models.TextChoices):
    admin = "admin", "Администратор"
    staff = "staff", "Сотрудник"
    user = "user", 'Пользователь'


class Category(models.TextChoices):
    electronics = 'electronics', 'электроника'
    books = 'books', 'книги'



