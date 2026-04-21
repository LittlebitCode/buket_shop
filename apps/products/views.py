from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category


@login_required
def shop_home(request):
    featured = Product.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()
    all_products = Product.objects.filter(is_available=True)

    category_slug = request.GET.get('category')
    search = request.GET.get('search', '')

    if category_slug:
        all_products = all_products.filter(category__slug=category_slug)
    if search:
        all_products = all_products.filter(name__icontains=search)

    context = {
        'featured': featured,
        'categories': categories,
        'products': all_products,
        'selected_category': category_slug,
        'search': search,
    }
    return render(request, 'shop/home.html', context)


@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product, 'related': related
    })


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
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

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items, 'total': total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    cart = request.session.get('cart', {})
    key = str(product_id)
    
    # Check if request is AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or \
              request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    if cart.get(key, 0) < product.stock:
        cart[key] = cart.get(key, 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
        
        message = f'{product.name} ditambahkan ke keranjang!'
        if is_ajax:
            return JsonResponse({
                'status': 'success',
                'message': message,
                'cart_count': sum(cart.values())
            })
        messages.success(request, message)
    else:
        message = f'Maaf, stok {product.name} tidak mencukupi.'
        if is_ajax:
            return JsonResponse({
                'status': 'error',
                'message': message
            }, status=400)
        messages.error(request, message)
        
    return redirect(request.META.get('HTTP_REFERER', 'shop_home'))


@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if qty <= 0:
        cart.pop(str(product_id), None)
    elif qty > product.stock:
        messages.error(request, f'Maksimal stok {product.name} adalah {product.stock}.')
        cart[str(product_id)] = product.stock
    else:
        cart[str(product_id)] = qty
    request.session['cart'] = cart
    return redirect('cart')
