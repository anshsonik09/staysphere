from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    FACILITY_TYPE_CHOICES = (
        ('swimming_pool', 'Swimming Pool'),
        ('gym', 'Gym'),
        ('spa', 'Spa'),
        ('gaming_zone', 'Gaming Zone'),
        ('conference_room', 'Conference Room'),
        ('banquet_hall', 'Banquet Hall'),
    )
    
    name = models.CharField(max_length=100)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES)
    description = models.TextField()
    capacity = models.PositiveIntegerField(help_text="Maximum number of people")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    operating_hours_start = models.TimeField()
    operating_hours_end = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_facility_type_display()}"
    
    @property
    def is_available_now(self):
        from django.utils import timezone
        current_time = timezone.now().time()
        return self.operating_hours_start <= current_time <= self.operating_hours_end and self.is_active

class FacilityBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    participants = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.customer.username} - {self.facility.name}"
    
    @property
    def duration_hours(self):
        from datetime import datetime
        start = datetime.strptime(str(self.start_time), '%H:%M:%S')
        end = datetime.strptime(str(self.end_time), '%H:%M:%S')
        return (end - start).seconds / 3600
    
    @property
    def is_active(self):
        return self.status in ['confirmed', 'in_progress']
    
    class Meta:
        verbose_name_plural = "Facility Bookings"
