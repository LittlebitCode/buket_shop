from django.urls import path
from . import api_views

urlpatterns = [
    path('products/', api_views.ProductListAPI.as_view(), name='api_products'),
    path('products/<int:pk>/', api_views.ProductDetailAPI.as_view(), name='api_product_detail'),
    path('categories/', api_views.CategoryListAPI.as_view(), name='api_categories'),
]
