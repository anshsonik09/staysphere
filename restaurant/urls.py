from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_home, name='restaurant_home'),
    path('menu/', views.menu, name='menu'),
    path('menu/<int:category_id>/', views.menu_category, name='menu_category'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('order/', views.place_order, name='place_order'),
    path('order/success/', views.order_success, name='order_success'),
    path('order/history/', views.order_history, name='order_history'),
    path('table-reservation/', views.table_reservation, name='table_reservation'),
    path('table-reservation/confirm/', views.table_reservation_confirm, name='table_reservation_confirm'),
]
