from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import json
from .models import MenuCategory, FoodItem, Order, OrderItem, Table, TableReservation

# Create your views here.

def restaurant_home(request):
    # Get featured menu items
    featured_items = FoodItem.objects.filter(is_available=True)[:6]
    categories = MenuCategory.objects.all()
    
    context = {
        'featured_items': featured_items,
        'categories': categories,
    }
    return render(request, 'restaurant/restaurant_home.html', context)

def menu(request):
    categories = MenuCategory.objects.all()
    food_items = FoodItem.objects.filter(is_available=True).select_related('category')
    
    category_id = request.GET.get('category')
    if category_id:
        food_items = food_items.filter(category_id=category_id)
    
    food_type = request.GET.get('type')
    if food_type:
        food_items = food_items.filter(food_type=food_type)
    
    search_query = request.GET.get('search')
    if search_query:
        food_items = food_items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': category_id,
        'selected_type': food_type,
        'search_query': search_query,
    }
    return render(request, 'restaurant/menu.html', context)

def menu_category(request, category_id):
    category = get_object_or_404(MenuCategory, id=category_id)
    food_items = FoodItem.objects.filter(category=category, is_available=True)
    
    context = {
        'category': category,
        'food_items': food_items,
    }
    return render(request, 'restaurant/menu_category.html', context)

@login_required
def cart(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    if cart:
        item_ids = cart.keys()
        food_items = FoodItem.objects.filter(id__in=item_ids, is_available=True)
        
        for item in food_items:
            quantity = cart[str(item.id)]
            subtotal = item.price * quantity
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total_amount += subtotal
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_count': len(cart_items)
    }
    return render(request, 'restaurant/cart.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            food_item = FoodItem.objects.get(id=item_id, is_available=True)
            cart = request.session.get('cart', {})
            
            if str(item_id) in cart:
                cart[str(item_id)] += quantity
            else:
                cart[str(item_id)] = quantity
            
            request.session['cart'] = cart
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': f'{food_item.name} added to cart!',
                'cart_count': sum(cart.values())
            })
            
        except FoodItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not available'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))
        
        cart = request.session.get('cart', {})
        
        if quantity <= 0:
            cart.pop(str(item_id), None)
        else:
            cart[str(item_id)] = quantity
        
        request.session['cart'] = cart
        request.session.modified = True
        
        # Calculate new total
        total_amount = 0
        if cart:
            item_ids = cart.keys()
            food_items = FoodItem.objects.filter(id__in=item_ids)
            for item in food_items:
                total_amount += item.price * cart[str(item.id)]
        
        return JsonResponse({
            'success': True,
            'total_amount': total_amount,
            'cart_count': sum(cart.values())
        })
    
    return JsonResponse({'success': False})

@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('menu')
    
    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        table_id = request.POST.get('table')
        room_number = request.POST.get('room_number')
        special_instructions = request.POST.get('special_instructions', '')
        
        # Create order
        order = Order.objects.create(
            customer=request.user,
            order_type=order_type,
            table_id=table_id if table_id else None,
            room_number=room_number if room_number else None,
            special_instructions=special_instructions,
            status='pending'
        )
        
        # Add items to order
        total_amount = 0
        item_ids = cart.keys()
        food_items = FoodItem.objects.filter(id__in=item_ids)
        
        for item in food_items:
            quantity = cart[str(item.id)]
            OrderItem.objects.create(
                order=order,
                food_item=item,
                quantity=quantity,
                price=item.price
            )
            total_amount += item.price * quantity
        
        order.total_amount = total_amount
        order.save()
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f'Order placed successfully! Order ID: {order.id}')
        return redirect('order_success')
    
    # GET request - show order form
    tables = Table.objects.filter(status='available')
    
    context = {
        'tables': tables,
        'order_types': Order.ORDER_TYPE_CHOICES,
    }
    return render(request, 'restaurant/place_order.html', context)

def order_success(request):
    return render(request, 'restaurant/order_success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'restaurant/order_history.html', context)

@login_required
def table_reservation(request):
    if request.method == 'POST':
        table_id = request.POST.get('table')
        reservation_date = request.POST.get('date')
        reservation_time = request.POST.get('time')
        guests = request.POST.get('guests')
        special_requests = request.POST.get('special_requests', '')
        
        # Create reservation
        reservation = TableReservation.objects.create(
            customer=request.user,
            table_id=table_id,
            date=reservation_date,
            time=reservation_time,
            guests=guests,
            special_requests=special_requests,
            status='pending'
        )
        
        messages.success(request, f'Table reservation confirmed! Reservation ID: {reservation.id}')
        return redirect('table_reservation_confirm')
    
    # GET request - show reservation form
    tables = Table.objects.filter(status='available')
    
    context = {
        'tables': tables,
    }
    return render(request, 'restaurant/table_reservation.html', context)

@login_required
def table_reservation_confirm(request):
    return render(request, 'restaurant/table_reservation_confirm.html')
