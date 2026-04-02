"""
Root URL configuration for TalentHeart Limited.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Public landing & about pages
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # App URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('services/', include('services.urls', namespace='services')),
    path('orders/',   include('orders.urls',   namespace='orders')),
    path('contact/',  include('contact.urls',  namespace='contact')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
