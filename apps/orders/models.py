from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('confirmed', 'Dikonfirmasi'),
        ('processing', 'Sedang Diproses'),
        ('shipped', 'Dikirim'),
        ('delivered', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    recipient_name = models.CharField(max_length=200)
    recipient_phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    delivery_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = 'BKT' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def subtotal(self):
        return self.price * self.quantity


class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.action}"
