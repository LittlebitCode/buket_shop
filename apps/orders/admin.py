from django.contrib import admin
from .models import Order, OrderItem, OrderLog

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]

@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    list_display = ['order', 'action', 'created_by', 'created_at']
