from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Order, OrderItem, OrderLog
from apps.products.models import Product


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Keranjang Anda kosong.')
        return redirect('cart')

    cart_items = []
    total = 0
    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            recipient_name=request.POST.get('recipient_name'),
            recipient_phone=request.POST.get('recipient_phone'),
            delivery_address=request.POST.get('delivery_address'),
            delivery_date=request.POST.get('delivery_date') or None,
            notes=request.POST.get('notes', ''),
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                price=item['product'].price,
                quantity=item['quantity'],
            )
            # Deduct stock
            if item['product'].stock >= item['quantity']:
                item['product'].stock -= item['quantity']
            else:
                item['product'].stock = 0
            item['product'].save()

        OrderLog.objects.create(
            order=order,
            action='Pesanan dibuat',
            description=f'Pesanan baru dari {request.user.username}',
            created_by=request.user
        )

        request.session['cart'] = {}
        messages.success(request, f'Pesanan #{order.order_number} berhasil dibuat!')
        return redirect('order_success', order_number=order.order_number)

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items, 'total': total
    })


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'shop/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    logs = order.logs.all()
    return render(request, 'shop/order_detail.html', {'order': order, 'logs': logs})
