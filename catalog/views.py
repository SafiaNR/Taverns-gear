from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Product, Category

def catalog(request):
    products = Product.objects.filter(stock__gt=0)
    
    category_slug = request.GET.get('category')
    sort = request.GET.get('sort', '-created_at')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    allowed_sorts = ['name', '-name', 'price', '-price', 'year', '-year', 'created_at', '-created_at']
    if sort in allowed_sorts:
        products = products.order_by(sort)
    else:
        products = products.order_by('-created_at')
        sort = '-created_at'
    
    categories = Category.objects.filter(products__stock__gt=0).distinct()
    
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'current_sort': sort,
    })

def product_detail(request, slug):
    """Детальная страница товара"""
    try:
        product = get_object_or_404(Product, slug=slug)
        
        if product.stock <= 0:
            return render(request, 'product_out_of_stock.html', {
                'product': product
            })
        
        similar_products = Product.objects.filter(
            category=product.category, 
            stock__gt=0
        ).exclude(id=product.id)[:4]
        
        return render(request, 'product_detail.html', {
            'product': product,
            'similar_products': similar_products,
        })
    except Http404:
        return render(request, 'product_not_found.html', status=404)