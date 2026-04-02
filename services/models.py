"""
services/models.py
Service catalogue for TalentHeart Limited.
"""
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    """A service offered by TalentHeart (e.g., Web Development)."""

    CATEGORY_CHOICES = [
        ('digital_marketing', 'Digital Marketing'),
        ('web_development',   'Web Development'),
        ('devops',            'DevOps'),
    ]

    name              = models.CharField(max_length=100)
    slug              = models.SlugField(max_length=120, unique=True, blank=True)
    category          = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    short_description = models.CharField(max_length=255, help_text='One-line summary shown on the listing page.')
    description       = models.TextField(help_text='Full description shown on the detail page.')
    price             = models.DecimalField(max_digits=10, decimal_places=2, help_text='Starting price in USD.')
    icon_class        = models.CharField(
        max_length=60, default='bi bi-stars',
        help_text='Bootstrap Icon class, e.g. "bi bi-graph-up"'
    )
    is_active         = models.BooleanField(default=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('services:detail', kwargs={'slug': self.slug})


class ServiceFeature(models.Model):
    """A bullet-point feature/benefit for a service."""

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=200)
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.service.name} — {self.feature}"
