from django.db import models
from django.conf import settings
from catalog.models import Product

class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_CONFIRMED, 'Подтвержден'),
        (STATUS_CANCELED, 'Отменен'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders', 
        verbose_name='Клиент'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    cancel_reason = models.TextField('Причина отмены', blank=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заказ №{self.id}'
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name='Товар')
    price = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    def get_cost(self):
        return self.price * self.quantity