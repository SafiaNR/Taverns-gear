from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Кол-во товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'year', 'created_at']
    list_filter = ['category', 'created_at', 'year']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock']
    list_per_page = 25
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'stock')
        }),
        ('Характеристики', {
            'fields': ('country', 'year', 'model'),
            'classes': ('collapse',)
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )