from django.contrib import admin
from .models import Invoice, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    readonly_fields = ('created_at',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'total_amount', 'payment_status', 'issue_date', 'due_date')
    list_filter = ('payment_status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'customer__username')
    readonly_fields = ('invoice_number', 'issue_date')
    date_hierarchy = 'issue_date'
    inlines = [PaymentInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'customer', 'booking')
        }),
        ('Charges', {
            'fields': ('room_charges', 'food_charges', 'facility_charges')
        }),
        ('Totals', {
            'fields': ('subtotal', 'gst_percentage', 'gst_amount', 'total_amount')
        }),
        ('Payment Details', {
            'fields': ('payment_status', 'payment_method', 'amount_paid')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'paid_date')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'payment_method', 'transaction_id', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('invoice__invoice_number', 'transaction_id')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
