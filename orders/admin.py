from django.contrib import admin

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_info', 'created_at', 'status', 'total_quantity', 'total_cost', 'actions_buttons']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_per_page = 20
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'cancel_reason')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_info(self, obj):
        """Отображение информации о пользователе"""
        full_name = obj.user.get_full_name()
        if full_name:
            return format_html(
                '<strong>{}</strong><br><span style="color: #666;">{}</span>',
                full_name,
                obj.user.email
            )
        return format_html(
            '<strong>{}</strong><br><span style="color: #666;">{}</span>',
            obj.user.username,
            obj.user.email
        )
    user_info.short_description = 'Клиент'
    
    def total_quantity(self, obj):
        return obj.get_total_quantity()
    total_quantity.short_description = 'Кол-во товаров'
    
    def total_cost(self, obj):
        return f'{obj.get_total_cost():.2f} ₽'
    total_cost.short_description = 'Сумма'
    
    def actions_buttons(self, obj):
        """Кнопки для смены статуса"""
        buttons = []
        if obj.status == 'new':
            buttons.append(f'<a class="button" href="/admin/orders/order/{obj.id}/confirm/" style="background: #28a745; color: white; padding: 5px 10px; text-decoration: none; margin-right: 5px;">✅ Подтвердить</a>')
            buttons.append(f'<a class="button" href="/admin/orders/order/{obj.id}/cancel/" style="background: #dc3545; color: white; padding: 5px 10px; text-decoration: none;">❌ Отменить</a>')
        elif obj.status == 'confirmed':
            buttons.append('<span style="color: #28a745;">✓ Подтвержден</span>')
        elif obj.status == 'canceled':
            buttons.append('<span style="color: #dc3545;">✗ Отменен</span>')
        return format_html(' '.join(buttons))
    actions_buttons.short_description = 'Действия'
    
    actions = ['confirm_orders', 'cancel_orders']
    
    def confirm_orders(self, request, queryset):
        """Подтвердить выбранные заказы"""
        updated = queryset.filter(status='new').update(status='confirmed')
        self.message_user(request, f'{updated} заказов подтверждено.')
    confirm_orders.short_description = 'Подтвердить выбранные заказы'
    
    def cancel_orders(self, request, queryset):
        """Отменить выбранные заказы"""
        updated = queryset.filter(status='new').update(status='canceled', cancel_reason='Отменен администратором')
        self.message_user(request, f'{updated} заказов отменено.')
    cancel_orders.short_description = 'Отменить выбранные заказы'
     
    actions = ['confirm_orders', 'cancel_orders']
    
    def confirm_orders(self, request, queryset):
        updated = queryset.filter(status='new').update(status='confirmed')
        self.message_user(request, f'{updated} заказов подтверждено.')
    confirm_orders.short_description = 'Подтвердить выбранные заказы'
    
    def cancel_orders(self, request, queryset):
        updated = queryset.filter(status='new').update(status='canceled', cancel_reason='Отменен администратором')
        self.message_user(request, f'{updated} заказов отменено.')
    cancel_orders.short_description = 'Отменить выбранные заказы'

    
    

    

    
