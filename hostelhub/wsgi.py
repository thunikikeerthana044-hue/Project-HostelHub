"""
WSGI config for hostelhub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelhub.settings')

django.setup()
try:
    call_command('migrate', interactive=False)
    # Auto-seed the database if it is empty
    from django.contrib.auth.models import User
    if not User.objects.exists():
        from seed_data import seed
        seed()
except Exception as e:
    print("Migration/Seeding failed during startup:", e)

application = get_wsgi_application()


