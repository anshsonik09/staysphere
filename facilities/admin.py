from django.contrib import admin
from .models import Facility, FacilityBooking

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'capacity', 'hourly_rate', 'is_active')
    list_filter = ('facility_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'facility_type', 'description')
        }),
        ('Capacity & Pricing', {
            'fields': ('capacity', 'hourly_rate')
        }),
        ('Operating Hours', {
            'fields': ('operating_hours_start', 'operating_hours_end')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(FacilityBooking)
class FacilityBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'facility', 'date', 'start_time', 'end_time', 'status', 'total_amount')
    list_filter = ('status', 'facility', 'date')
    search_fields = ('customer__username', 'facility__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
