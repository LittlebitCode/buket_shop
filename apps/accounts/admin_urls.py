from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.dashboard, name='admin_dashboard'),
    path('orders/', admin_views.orders_list, name='admin_orders'),
    path('orders/<int:pk>/', admin_views.order_detail, name='admin_order_detail'),
    path('logs/', admin_views.order_logs, name='admin_logs'),
    path('products/', admin_views.products_manage, name='admin_products'),
    path('products/<int:pk>/toggle/', admin_views.product_toggle, name='admin_product_toggle'),
    path('orders/<int:pk>/delete/', admin_views.order_delete, name='admin_order_delete'),
    path('profile/', admin_views.admin_profile, name='admin_profile'),
]
