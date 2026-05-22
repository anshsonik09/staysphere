from django.contrib import admin
from .models import RoomCategory, Room, Booking

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'max_occupancy', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'category', 'floor', 'status', 'is_available')
    list_filter = ('status', 'category', 'floor')
    search_fields = ('room_number', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Room Information', {
            'fields': ('room_number', 'category', 'floor')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Details', {
            'fields': ('description', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'room', 'check_in', 'check_out', 'status', 'total_amount')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('customer__username', 'room__room_number')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'check_in'
