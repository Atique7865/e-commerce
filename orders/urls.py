"""
orders/urls.py
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('',                      views.order_list,   name='list'),
    path('new/',                  views.order_create, name='create'),
    path('new/<slug:slug>/',      views.order_create, name='create_for_service'),
    path('<int:pk>/',             views.order_detail, name='detail'),
    path('<int:pk>/cancel/',      views.order_cancel, name='cancel'),
]
