from django.contrib import admin
from .models import MenuCategory, FoodItem, Table, Order, OrderItem, TableReservation

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'food_type', 'is_available')
    list_filter = ('food_type', 'is_available', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing & Type', {
            'fields': ('price', 'food_type')
        }),
        ('Details', {
            'fields': ('image', 'preparation_time', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'location', 'status', 'is_available')
    list_filter = ('status', 'location')
    search_fields = ('table_number', 'location')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('subtotal',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_type', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'order_type', 'created_at')
    search_fields = ('customer__username', 'table__table_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'

@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'table', 'date', 'time', 'guests', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__username', 'table__table_number')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
