from django.db import models
from django.contrib.auth.models import User
from booking.models import Booking
from restaurant.models import Order

class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('wallet', 'Digital Wallet'),
    )
    
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    orders = models.ManyToManyField(Order, blank=True)
    
    # Billing details
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    food_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    facility_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment details
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    paid_date = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_invoices')
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.username}"
    
    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now().date() and self.payment_status != 'paid'
    
    def calculate_totals(self):
        self.subtotal = self.room_charges + self.food_charges + self.facility_charges
        self.gst_amount = (self.subtotal * self.gst_percentage) / 100
        self.total_amount = self.subtotal + self.gst_amount
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from django.utils import timezone
            year = timezone.now().year
            month = timezone.now().month
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=f'INV{year}{month:02d}'
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_number = int(last_invoice.invoice_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.invoice_number = f'INV{year}{month:02d}{new_number:04d}'
        
        super().save(*args, **kwargs)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Invoice.PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.invoice.invoice_number} - {self.amount}"
