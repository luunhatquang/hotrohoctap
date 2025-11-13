#!/usr/bin/env python
"""
Script để export data từ MySQL local ra file JSON
Dùng để chuyển data lên database online
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchuniversity.settings')
django.setup()

from django.core.management import call_command

def export_data():
    """Export tất cả data ra file JSON"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data_export_{timestamp}.json'
    
    print(f"📤 Đang export data...")
    print(f"📁 File: {filename}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--indent', '2',
            '--exclude', 'contenttypes',
            '--exclude', 'auth.permission',
            '--exclude', 'sessions',
            '--exclude', 'admin.logentry',
            stdout=f
        )
    
    # Lấy kích thước file
    size = os.path.getsize(filename)
    size_kb = size / 1024
    
    print(f"✅ Export thành công!")
    print(f"📊 Kích thước: {size_kb:.1f} KB")
    print(f"\n📝 Để import lên database online:")
    print(f"   1. Cập nhật .env với thông tin database online")
    print(f"   2. Chạy: python manage.py migrate")
    print(f"   3. Chạy: python manage.py loaddata {filename}")

if __name__ == '__main__':
    try:
        export_data()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)

