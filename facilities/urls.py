from django.urls import path
from . import views

urlpatterns = [
    path('', views.facilities_home, name='facilities_home'),
    path('facility/<int:facility_id>/', views.facility_detail, name='facility_detail'),
    path('facility/<int:facility_id>/book/', views.facility_booking, name='facility_booking'),
    path('booking/success/', views.facility_booking_success, name='facility_booking_success'),
    path('my-bookings/', views.facility_bookings, name='facility_bookings'),
]
