from django.db import models
from django.contrib.auth.models import User

class RoomCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Room Categories"

class Room(models.Model):
    ROOM_STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    )
    
    room_number = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Room {self.room_number} - {self.category.name}"
    
    @property
    def is_available(self):
        return self.status == 'available'

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.customer.username} - Room {self.room.room_number}"
    
    @property
    def total_nights(self):
        return (self.check_out - self.check_in).days
    
    @property
    def is_active(self):
        return self.status in ['confirmed', 'checked_in']

