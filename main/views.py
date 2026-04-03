from django.shortcuts import render
from catalog.models import Product

def about(request):
    """Страница 'О нас' с новинками (только товары в наличии)"""
    new_products = Product.objects.filter(stock__gt=0).order_by('-created_at')[:5]
    
    return render(request, 'about.html', {
        'new_products': new_products,
    })

def contacts(request):
    """Страница 'Где нас найти?'"""
    return render(request, 'contacts.html')