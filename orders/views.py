from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
from .models import Order, OrderItem
from cart.cart import Cart

@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.error(request, 'Корзина пуста')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            # Создаем заказ
            order = Order.objects.create(user=user)
            
            for item in cart:
                product = item['product']
                if product.stock >= item['quantity']:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    # Уменьшаем количество на складе
                    product.stock -= item['quantity']
                    product.save()
                else:
                    order.delete()
                    return JsonResponse({
                        'success': False,
                        'error': f'Товара "{product.name}" нет в нужном количестве'
                    })
            
            cart.clear()
            return JsonResponse({
                'success': True,
                'redirect_url': f'/orders/{order.id}/'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Неверный пароль'
            })
    
    return render(request, 'order_create.html', {'cart': cart})

@require_POST
@login_required
def order_delete(request):
    """Удаление заказа"""
    order_id = request.POST.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Можно удалить только новые заказы
    if order.status == 'new':
        order.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Можно удалить только новые заказы'})
