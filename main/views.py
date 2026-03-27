from django.shortcuts import render
from catalog.models import Product

def about(request):
    new_products = Product.objects.all().order_by('-created_at')[:5]
    print(f"Товаров в новинках: {new_products.count()}")  # Для отладки
    return render(request, 'about.html', {'new_products': new_products})

def contacts(request):
    """Страница 'Где нас найти?'"""
    return render(request, 'contacts.html')