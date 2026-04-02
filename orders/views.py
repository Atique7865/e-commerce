"""
orders/views.py
CRUD views for client orders. All views require authentication.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from services.models import Service
from .models import Order
from .forms import OrderForm


@login_required
def order_list(request):
    """Show all orders belonging to the logged-in user."""
    orders = Order.objects.filter(user=request.user).select_related('service')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_create(request, slug=None):
    """Create a new order, optionally pre-selecting a service via slug."""
    service = None
    if slug:
        service = get_object_or_404(Service, slug=slug, is_active=True)

    if request.method == 'POST':
        form = OrderForm(request.POST, service=service)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(
                request,
                f'Your order for "{order.service.name}" has been submitted! '
                'Our team will be in touch shortly.'
            )
            return redirect('orders:detail', pk=order.pk)
    else:
        form = OrderForm(service=service)

    return render(request, 'orders/create.html', {
        'form':    form,
        'service': service,
    })


@login_required
def order_detail(request, pk):
    """View a single order (owner only)."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def order_cancel(request, pk):
    """Cancel a pending order (POST only)."""
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status not in ('pending', 'in_progress'):
        messages.warning(request, 'This order cannot be cancelled.')
        return redirect('orders:detail', pk=order.pk)

    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.pk} has been cancelled.')
        return redirect('orders:list')

    return render(request, 'orders/cancel_confirm.html', {'order': order})
