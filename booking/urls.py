from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('category/<int:category_id>/', views.room_detail, name='room_detail'),
    path('booking/', views.booking_form, name='booking_form'),
    path('booking/confirm/', views.booking_confirm, name='booking_confirm'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('contact/', views.contact, name='contact'),
]
