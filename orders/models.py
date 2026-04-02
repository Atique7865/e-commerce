"""
orders/models.py
Order/booking model — links a client to a TalentHeart service.
"""
from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Order(models.Model):
    """A client's booking/order for a specific service."""

    STATUS_CHOICES = [
        ('pending',     'Pending Review'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
        ('cancelled',   'Cancelled'),
    ]

    BUDGET_CHOICES = [
        ('under_1k',   'Under $1,000'),
        ('1k_5k',      '$1,000 – $5,000'),
        ('5k_10k',     '$5,000 – $10,000'),
        ('10k_plus',   '$10,000+'),
        ('discuss',    'Let\'s Discuss'),
    ]

    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service            = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='orders')
    status             = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    budget_range       = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='discuss')
    project_name       = models.CharField(max_length=150, help_text='Short name for this project.')
    project_description = models.TextField(help_text='Describe what you need in detail.')
    deadline           = models.DateField(null=True, blank=True, help_text='Desired completion date (optional).')
    admin_notes        = models.TextField(blank=True, help_text='Internal notes (visible to staff only).')
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.pk} — {self.service.name} ({self.user.username})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('orders:detail', kwargs={'pk': self.pk})

    @property
    def status_badge_class(self):
        """Return a Bootstrap badge class based on status."""
        mapping = {
            'pending':     'bg-warning text-dark',
            'in_progress': 'bg-primary',
            'completed':   'bg-success',
            'cancelled':   'bg-danger',
        }
        return mapping.get(self.status, 'bg-secondary')
