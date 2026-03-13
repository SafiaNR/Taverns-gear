from django.shortcuts import render
from .models import Product, Category

def catalog(request):
    products = Product.objects.filter(stock__gt=0)
    
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    sort = request.GET.get('sort', '-created_at')
    if sort in ['name', '-name', 'price', '-price', 'year', '-year', 'created_at', '-created_at']:
        products = products.order_by(sort)
    else:
        products = products.order_by('-created_at')
    
    categories = Category.objects.all()
    
    return render(request, 'catalog.html', {  
        'products': products,
        'categories': categories,
        'selected_category': category_slug
    })
