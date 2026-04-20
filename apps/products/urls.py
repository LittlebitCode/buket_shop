from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('produk/<slug:slug>/', views.product_detail, name='product_detail'),
    path('keranjang/', views.cart_view, name='cart'),
    path('keranjang/tambah/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('keranjang/hapus/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('keranjang/update/<int:product_id>/', views.update_cart, name='update_cart'),
]
