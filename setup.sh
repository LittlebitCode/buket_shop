#!/bin/bash
# ============================================================
#  A&A Bouquet — Setup & Run Script
#  Jalankan: bash setup.sh
# ============================================================

set -e

echo ""
echo "🌸 ========================================"
echo "   A&A Bouquet — Web Penjualan Buket"
echo "   Setup & Run Script"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Install Python 3.8+ terlebih dahulu."
    exit 1
fi

echo "✓ Python: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Membuat virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment dibuat"
fi

# Activate venv
source venv/bin/activate
echo "✓ Virtual environment aktif"

# Install dependencies
echo ""
echo "📥 Menginstall dependensi..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Semua dependensi terinstall"

# Run migrations
echo ""
echo "🗄️  Membuat database..."
python manage.py makemigrations accounts 2>/dev/null || true
python manage.py makemigrations products orders 2>/dev/null || true
python manage.py makemigrations 2>/dev/null || true
python manage.py migrate
echo "✓ Database siap"

# Create media dirs
mkdir -p media/products
echo "✓ Direktori media dibuat"

# Seed data
echo ""
echo "🌱 Mengisi data awal..."
python seed_data.py

# Collect static (optional)
# python manage.py collectstatic --noinput

echo ""
echo "🎉 ========================================"
echo "   Setup selesai! Jalankan server:"
echo ""
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "   Buka: http://127.0.0.1:8000"
echo ""
echo "   Login Admin:   admin / admin123"
echo "   Login Pembeli: pelanggan1 / user123"
echo "=========================================="
echo ""
