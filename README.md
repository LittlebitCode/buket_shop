# 🌸 A&A Bouquet — Web Penjualan Buket

Aplikasi web penjualan buket berbasis **Django + HTMX/Vanilla JS** dengan UI premium dan dua mode akses: **Pembeli** dan **Admin**.

---

## 🚀 Cara Menjalankan

### 1. Clone / Download project
```
buket_shop/
├── buket_shop/          # Konfigurasi Django
├── apps/
│   ├── products/        # Produk & kategori
│   ├── orders/          # Pesanan & log
│   └── accounts/        # Auth & admin panel
├── templates/           # HTML templates
├── static/              # CSS, JS, gambar
├── requirements.txt
├── setup.sh             # Script otomatis
└── seed_data.py         # Data demo
```

### 2. Setup otomatis (Linux/Mac)
```bash
cd buket_shop
bash setup.sh
python manage.py runserver
```

### 3. Setup manual (Windows / manual)
```bash
cd buket_shop

# Buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# atau
source venv/bin/activate     # Linux/Mac

# Install dependensi
pip install -r requirements.txt

# Buat & migrasi database
python manage.py makemigrations products orders accounts
python manage.py migrate

# Isi data demo
python seed_data.py

# Jalankan server
python manage.py runserver
```

### 4. Buka di browser
```
http://127.0.0.1:8000
```

---

## 🔑 Akun Demo

| Role    | Username     | Password  | Akses                    |
|---------|-------------|-----------|--------------------------|
| Admin   | `admin`     | `admin123`| Admin panel + semua fitur|
| Pembeli | `pelanggan1`| `user123` | Toko + pesanan sendiri   |

---

## 🗺️ Halaman Utama

### Halaman Publik / Pembeli
| URL | Halaman |
|-----|---------|
| `/` | Beranda toko |
| `/auth/login/` | Halaman login (pilih peran) |
| `/auth/register/` | Halaman daftar akun |
| `/produk/<slug>/` | Detail produk |
| `/keranjang/` | Keranjang belanja |
| `/orders/checkout/` | Checkout |
| `/orders/pesanan-saya/` | Riwayat pesanan |

### Admin Panel
| URL | Halaman |
|-----|---------|
| `/admin-panel/` | Dashboard + grafik |
| `/admin-panel/orders/` | Daftar semua pesanan |
| `/admin-panel/orders/<id>/` | Detail + update status |
| `/admin-panel/logs/` | Log aktivitas pesanan |
| `/admin-panel/products/` | Kelola produk |
| `/django-admin/` | Django Admin (CRUD penuh) |

---

## ✨ Fitur

### Untuk Pembeli
- ✅ Register & Login
- ✅ Browse produk dengan filter kategori & pencarian
- ✅ Halaman detail produk
- ✅ Keranjang belanja (session-based)
- ✅ Checkout dengan data pengiriman
- ✅ Riwayat & detail pesanan
- ✅ Timeline status pesanan

### Untuk Admin
- ✅ Dashboard dengan grafik pesanan & pendapatan (Chart.js)
- ✅ Grafik bar & line 14 hari terakhir
- ✅ Donut chart status pesanan
- ✅ Manajemen pesanan (filter + search)
- ✅ Update status pesanan dengan catatan
- ✅ Log aktivitas lengkap
- ✅ Toggle aktif/nonaktif produk

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Django 4.2 + Django REST Framework |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Frontend | HTML/CSS + Vanilla JS |
| Charts | Chart.js 4 (CDN) |
| Auth | Django built-in auth + DRF Token |
| Font | Cormorant Garamond + DM Sans |

---

## 📦 Menambah Produk

1. Buka `http://127.0.0.1:8000/django-admin/`
2. Login dengan akun admin
3. Pergi ke **Products → Add Product**
4. Isi nama, slug, kategori, harga, stok, gambar
5. Centang **Is available** dan **Is featured** jika perlu

---

## 🚢 Deploy ke Production

1. Ubah `DEBUG = False` di `settings.py`
2. Ganti `SECRET_KEY` dengan nilai aman
3. Gunakan PostgreSQL untuk database
4. Jalankan `python manage.py collectstatic`
5. Gunakan Nginx + Gunicorn

```bash
pip install gunicorn psycopg2-binary
gunicorn buket_shop.wsgi:application --bind 0.0.0.0:8000
```

---

## 📝 Catatan Pengembangan

- Untuk gambar produk: upload melalui Django Admin
- File media tersimpan di folder `media/`
- Log pesanan otomatis dibuat setiap ada perubahan status
- Cart menggunakan Django session (tidak perlu login ulang)
- API endpoint tersedia di `/api/` dan `/api/orders/`

---

*Dibuat dengan ❤️ menggunakan Django + CSS custom design system*
