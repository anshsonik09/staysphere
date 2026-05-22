from django.db import models
from django.contrib.auth.models import User

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='menu_categories/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Menu Categories"

class FoodItem(models.Model):
    FOOD_TYPE_CHOICES = (
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
    )
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.category.name}"

class Table(models.Model):
    TABLE_STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    )
    
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=50, help_text="e.g., Ground Floor, Terrace")
    status = models.CharField(max_length=20, choices=TABLE_STATUS_CHOICES, default='available')
    
    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} seats)"
    
    @property
    def is_available(self):
        return self.status == 'available'

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    ORDER_TYPE_CHOICES = (
        ('dine_in', 'Dine In'),
        ('room_delivery', 'Room Delivery'),
        ('takeaway', 'Takeaway'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    room_number = models.CharField(max_length=10, blank=True, null=True, help_text="For room delivery")
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.get_order_type_display()}"
    
    @property
    def is_completed(self):
        return self.status == 'delivered'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"
    
    @property
    def subtotal(self):
        return self.quantity * self.price

class TableReservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reservation {self.id} - {self.customer.username} - {self.date}"
    
    class Meta:
        verbose_name_plural = "Table Reservations"
