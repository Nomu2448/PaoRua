import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PaoRua.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '123456')
    print('Created admin:123456')
else:
    print('User admin already exists')