from django.urls import path
from . import views

urlpatterns = [
    path('', views.reception_dashboard, name='reception_dashboard'),
    path('check-in/<int:booking_id>/', views.check_in, name='check_in'),
    path('check-out/<int:booking_id>/', views.check_out, name='check_out'),
    path('walk-in/', views.walk_in_registration, name='walk_in_registration'),
    path('rooms/', views.room_management, name='room_management'),
    path('bookings/', views.all_bookings, name='all_bookings'),
    path('search/', views.search_booking, name='search_booking'),
    path('invoice/create/<int:booking_id>/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/success/', views.invoice_success, name='invoice_success'),
]
