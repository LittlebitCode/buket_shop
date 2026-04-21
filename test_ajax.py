import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buket_shop.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from apps.products.models import Product

# Create a test user if none
user, _ = User.objects.get_or_create(username='testuser')
user.set_password('password123')
user.save()

client = Client()
client.login(username='testuser', password='password123')

p = Product.objects.first()
print(f"Testing with product {p.id} - {p.name}")

response = client.post(
    f'/keranjang/tambah/{p.id}/',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
)

print(f"Response status: {response.status_code}")
print(f"Response content: {response.content}")

# check session cart
session = client.session
print(f"Session cart: {session.get('cart')}")
