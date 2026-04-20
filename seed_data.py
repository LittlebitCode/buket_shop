"""
Seed script to populate demo data.
Run: python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buket_shop.settings')
django.setup()

from django.contrib.auth.models import User
from apps.products.models import Product, Category
from apps.orders.models import Order, OrderItem, OrderLog

print("🌸 Seeding A&A Bouquet database...")

# ── CATEGORIES ─────────────────────────────────────────────
cats = [
    ("Buket Mawar", "buket-mawar"),
    ("Buket Tulip", "buket-tulip"),
    ("Buket Wisuda", "buket-wisuda"),
    ("Buket Pernikahan", "buket-pernikahan"),
    ("Buket Ulang Tahun", "buket-ulang-tahun"),
    ("Buket Sunflower", "buket-sunflower"),
]
category_objs = {}
for name, slug in cats:
    cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": f"Koleksi {name} terbaik"})
    category_objs[slug] = cat
    print(f"  ✓ Kategori: {name}")

# ── PRODUCTS ────────────────────────────────────────────────
products_data = [
    ("Grand Rose Bouquet", "grand-rose-bouquet", "buket-mawar", 250000, 15, True,
     "Buket mawar merah premium dengan 24 tangkai, dibungkus kertas kraft eksklusif dan pita satin. Cocok untuk hadiah ulang tahun, anniversary, atau ungkapan cinta."),
    ("Pastel Dream", "pastel-dream", "buket-mawar", 185000, 20, True,
     "Kombinasi mawar pink muda, peach, dan putih yang memukau. Tampilan lembut dan elegan, cocok untuk wisuda atau hari ibu."),
    ("Tulip Romance", "tulip-romance", "buket-tulip", 220000, 10, True,
     "Buket tulip segar pilihan dari kebun terbaik. Tersedia dalam berbagai warna — merah, kuning, ungu, dan pink."),
    ("Sunflower Joy", "sunflower-joy", "buket-sunflower", 175000, 18, False,
     "Buket bunga matahari cerah yang memancarkan kebahagiaan. Pilihan sempurna untuk ucapan selamat dan semangat."),
    ("Wedding White", "wedding-white", "buket-pernikahan", 450000, 5, True,
     "Buket pengantin eksklusif dengan mawar putih, baby breath, dan eucalyptus. Dirancang khusus untuk hari pernikahan impian."),
    ("Graduation Glory", "graduation-glory", "buket-wisuda", 200000, 25, False,
     "Buket wisuda meriah dengan kombinasi bunga warna-warni dan aksesori bintang. Rayakan pencapaianmu dengan penuh gaya!"),
    ("Birthday Bliss", "birthday-bliss", "buket-ulang-tahun", 195000, 12, True,
     "Buket ulang tahun ceria dengan mix bunga seasonal, balon mini, dan kartu ucapan eksklusif dari A&A Bouquet."),
    ("Lavender Dreams", "lavender-dreams", "buket-mawar", 165000, 8, False,
     "Buket mawar lavender dan ungu yang romantis. Diperkaya dengan tanaman hijau dan dried flowers untuk kesan bohemian."),
    ("Mini Surprise", "mini-surprise", "buket-ulang-tahun", 125000, 30, False,
     "Buket kecil nan imut untuk kejutan mendadak. Compact, cantik, dan tetap penuh makna."),
    ("Tropical Fiesta", "tropical-fiesta", "buket-sunflower", 230000, 7, True,
     "Perpaduan sunflower, heliconia, dan bunga tropis eksotis. Tampil beda dengan nuansa segar dan cerah."),
    ("Pink Royale", "pink-royale", "buket-mawar", 280000, 10, True,
     "36 tangkai mawar pink premium dalam kotak eksklusif. Pilihan mewah untuk momen spesial yang tak terlupakan."),
    ("Tulip Carnival", "tulip-carnival", "buket-tulip", 210000, 14, False,
     "Pesta warna-warni dengan 20 tulip multi-warna. Meriah, segar, dan membuat siapapun tersenyum bahagia."),
]

for name, slug, cat_slug, price, stock, featured, desc in products_data:
    prod, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "category": category_objs[cat_slug],
            "price": price,
            "stock": stock,
            "is_featured": featured,
            "is_available": True,
            "description": desc,
        }
    )
    status = "✓ Baru" if created else "→ Ada"
    print(f"  {status} Produk: {name}")

# ── USERS ───────────────────────────────────────────────────
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@aandabouquet.id", "admin123",
                                  first_name="Admin", last_name="A&A Bouquet")
    print("  ✓ Admin: admin / admin123")
else:
    print("  → Admin sudah ada")

if not User.objects.filter(username="pelanggan1").exists():
    user = User.objects.create_user("pelanggan1", "pelanggan@aandabouquet.id", "user123",
                                    first_name="Sari", last_name="Dewi")
    print("  ✓ User: pelanggan1 / user123")
else:
    user = User.objects.get(username="pelanggan1")
    print("  → pelanggan1 sudah ada")

# ── SAMPLE ORDERS ───────────────────────────────────────────
if not Order.objects.filter(user=user).exists():
    from decimal import Decimal
    prods = list(Product.objects.all()[:3])

    statuses = ["delivered", "processing", "pending"]
    for i, status in enumerate(statuses):
        prod = prods[i]
        order = Order.objects.create(
            user=user,
            total_price=Decimal(prod.price) * (i + 1),
            status=status,
            recipient_name="Sari Dewi",
            recipient_phone="08123456789",
            delivery_address="Jl. Bunga Melati No. 12, Kebayoran Baru, Jakarta Selatan 12180",
        )
        OrderItem.objects.create(
            order=order,
            product=prod,
            product_name=prod.name,
            price=prod.price,
            quantity=i + 1,
        )
        admin_user = User.objects.filter(is_superuser=True).first()
        OrderLog.objects.create(
            order=order,
            action="Pesanan dibuat",
            description=f"Pesanan baru dari {user.username}",
            created_by=user
        )
        if status in ["processing", "delivered"]:
            OrderLog.objects.create(
                order=order,
                action="Status diubah ke Dikonfirmasi",
                description="Pesanan telah dikonfirmasi oleh admin.",
                created_by=admin_user
            )
        if status == "delivered":
            OrderLog.objects.create(
                order=order,
                action="Status diubah ke Selesai",
                description="Pesanan telah diterima oleh pelanggan.",
                created_by=admin_user
            )
        print(f"  ✓ Sample order #{order.order_number} [{status}]")
else:
    print("  → Sample orders sudah ada")

print("\n✅ Seeding selesai!")
print("\n📌 Akun login:")
print("   Admin   → username: admin    | password: admin123")
print("   Pembeli → username: pelanggan1 | password: user123")
print("\n🚀 Jalankan: python manage.py runserver")
