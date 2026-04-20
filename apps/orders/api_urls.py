from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.OrderListAPI.as_view(), name='api_orders'),
    path('<int:pk>/', api_views.OrderDetailAPI.as_view(), name='api_order_detail'),
]
