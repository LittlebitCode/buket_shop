from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, TruncDay, TruncDate
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from datetime import timedelta
import json

from apps.orders.models import Order, OrderLog
from apps.products.models import Product, Category


@staff_member_required(login_url='/auth/login/')
def dashboard(request):
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_price'))['total'] or 0
    total_products = Product.objects.count()

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:8]

    # Chart data - last 14 days
    start_date = (today - timedelta(days=13)).date()
    
    # Query database directly instead of 28 separate queries
    daily_stats = Order.objects.filter(
        created_at__date__gte=start_date
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        orders_count=Count('id'),
        revenue=Sum('total_price', filter=Q(status='delivered'))
    )
    
    stats_dict = {
        item['date']: item
        for item in daily_stats
    }

    chart_data = []
    for i in range(13, -1, -1):
        day = (today - timedelta(days=i)).date()
        day_stats = stats_dict.get(day, {'orders_count': 0, 'revenue': 0})
        
        chart_data.append({
            'date': day.strftime('%d %b'),
            'orders': day_stats['orders_count'],
            'revenue': float(day_stats['revenue'] or 0),
        })

    # Status breakdown
    status_data = Order.objects.values('status').annotate(count=Count('id'))

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'chart_data_json': json.dumps(chart_data),
        'status_data': list(status_data),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required(login_url='/auth/login/')
def orders_list(request):
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')

    orders = Order.objects.select_related('user').prefetch_related('items')

    if status_filter:
        orders = orders.filter(status=status_filter)
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(user__username__icontains=search) |
            Q(recipient_name__icontains=search)
        )

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'admin_panel/orders.html', context)


@staff_member_required(login_url='/auth/login/')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    logs = order.logs.select_related('created_by').all()

    if request.method == 'POST':
        new_status = request.POST.get('status')
        note = request.POST.get('note', '')
        if new_status and new_status != order.status:
            old_status = order.get_status_display()
            order.status = new_status
            order.save()
            OrderLog.objects.create(
                order=order,
                action=f'Status diubah ke {order.get_status_display()}',
                description=f'Dari: {old_status}. {note}',
                created_by=request.user
            )
        return redirect('admin_order_detail', pk=pk)

    return render(request, 'admin_panel/order_detail.html', {'order': order, 'logs': logs})


@staff_member_required(login_url='/auth/login/')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('admin_orders')
    return redirect('admin_order_detail', pk=pk)


@staff_member_required(login_url='/auth/login/')
def order_logs(request):
    logs = OrderLog.objects.select_related('order', 'created_by').order_by('-created_at')[:100]
    return render(request, 'admin_panel/logs.html', {'logs': logs})


@staff_member_required(login_url='/auth/login/')
def products_manage(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    return render(request, 'admin_panel/products.html', {'products': products, 'categories': categories})


@staff_member_required(login_url='/auth/login/')
def product_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_available = not product.is_available
    product.save()
    return redirect('admin_products')


@staff_member_required(login_url='/auth/login/')
def admin_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        
        # Validation for username
        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return redirect('admin_profile')

        user.username = username
        user.first_name = first_name
        user.email = email
        
        if new_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
        else:
            user.save()
            
        messages.success(request, 'Profil admin berhasil diperbarui!')
        return redirect('admin_profile')
        
    return render(request, 'admin_panel/profile.html', {'user': user})
