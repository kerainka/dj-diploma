from django.db import models
from django.conf import settings


class TimestampFields(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )


class Product(TimestampFields):
    name = models.CharField(max_length=50, verbose_name="Название")
    desc = models.TextField(max_length=200, verbose_name="Описание")
    price = models.DecimalField(max_digits=15, verbose_name="Цена")

    class Meta:
        verbose_name_plural = 'products'
        verbose_name = 'product'

    def __str__(self):
        return self.name


class Review(TimestampFields):
    review = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True, related_name='reviews',
        verbose_name="Товар")

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='users'
    )

    text = models.TextField(max_length=100, verbose_name="Отзыв")
    CHOICES = (
        (1, 'Плохо'),
        (2, 'Неудовлетворительно'),
        (3, 'Удовлетворительно'),
        (4, 'Хорошо'),
        (5, 'Отлично')
    )
    rating = models.IntegerField(choices=CHOICES, default=1, verbose_name="Оценка")

    class Meta:
        verbose_name_plural = 'product-reviews'
        verbose_name = 'product-reviews'


class ProductPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товары")
    order = models.ForeignKey("Orders", related_name='positions', on_delete=models.CASCADE, verbose_name="Заказ")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def get_cost(self):
        return self.product.price * self.quantity


class Order(TimestampFields):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='users'
    )

    STATUS = (
        'NEW',
        'IN_PROGRESS',
        'DONE'
    )

    status = models.CharField(choices=STATUS, default=1, verbose_name="Статус")
    products = models.ManyToManyField(Product, through=ProductPosition, verbose_name="Товары")

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.positions.all())

    order_sum = property(get_total_cost)

    class Meta:
        verbose_name_plural = 'orders'
        verbose_name = 'order'
        ordering = ['-created_at']


class Collection(TimestampFields):
    title = models.CharField(max_length=50,  verbose_name="Заголовок")
    text = models.TextField(max_length=100, verbose_name="Описание")
    products = models.ManyToManyField(Product, verbose_name="Товары")

    class Meta:
        verbose_name_plural = 'collections'
        verbose_name = 'collection'

    def __str__(self):
        return self.title
