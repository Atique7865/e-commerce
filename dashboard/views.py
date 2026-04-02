"""
dashboard/views.py
Client dashboard — shows an overview of the user's orders and account status.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from orders.models import Order
from services.models import Service


@login_required
def dashboard_index(request):
    """Main client dashboard view."""
    user_orders = Order.objects.filter(user=request.user).select_related('service')

    # Aggregate order counts per status
    stats = user_orders.aggregate(
        total=Count('id'),
    )
    stats['pending']     = user_orders.filter(status='pending').count()
    stats['in_progress'] = user_orders.filter(status='in_progress').count()
    stats['completed']   = user_orders.filter(status='completed').count()
    stats['cancelled']   = user_orders.filter(status='cancelled').count()

    recent_orders  = user_orders[:5]
    all_services   = Service.objects.filter(is_active=True)[:3]

    return render(request, 'dashboard/dashboard.html', {
        'stats':         stats,
        'recent_orders': recent_orders,
        'services':      all_services,
    })
