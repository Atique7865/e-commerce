"""ASGI config for TalentHeart Limited."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentheart.settings')
application = get_asgi_application()
