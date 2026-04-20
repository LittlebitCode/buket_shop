from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('sukses/<str:order_number>/', views.order_success, name='order_success'),
    path('pesanan-saya/', views.my_orders, name='my_orders'),
    path('pesanan/<str:order_number>/', views.order_detail, name='order_detail'),
]
