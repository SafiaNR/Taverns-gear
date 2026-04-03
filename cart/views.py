from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart

@login_required
def cart_detail(request):
    """Просмотр корзины"""
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

@require_POST
@login_required
def cart_add(request):
    """Добавление товара в корзину"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        
        current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
        if current_quantity + quantity > product.stock:
            return JsonResponse({
                'success': False,
                'error': f'Нельзя добавить больше {product.stock} шт. товара "{product.name}"'
            })
        
        cart.add(product=product, quantity=quantity, update_quantity=False)
        
        return JsonResponse({
            'success': True,
            'cart_total': len(cart),
            'message': f'Товар "{product.name}" добавлен в корзину'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_POST
@login_required
def cart_update(request):
    """Обновление количества товара в корзине"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    
    if quantity > product.stock:
        return JsonResponse({
            'success': False,
            'error': f'Недостаточно товара. В наличии: {product.stock} шт.'
        })
    
    cart.add(product=product, quantity=quantity, update_quantity=True)
    
    return JsonResponse({
        'success': True,
        'total_items': len(cart),
        'total_price': str(cart.get_total_price())
    })

@require_POST
@login_required
def cart_remove(request):
    """Удаление товара из корзины"""
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    
    return JsonResponse({
        'success': True,
        'total_items': len(cart),
        'total_price': str(cart.get_total_price())
    })
