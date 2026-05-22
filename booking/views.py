from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date
from .models import RoomCategory, Room, Booking
from accounts.models import UserProfile

# Create your views here.

def home(request):
    # Get featured rooms for homepage
    featured_rooms = Room.objects.filter(status='available')[:3]
    room_categories = RoomCategory.objects.all()[:4]
    
    context = {
        'featured_rooms': featured_rooms,
        'room_categories': room_categories,
    }
    return render(request, 'booking/home.html', context)

def room_list(request):
    # Get all room categories
    categories = RoomCategory.objects.all()
    
    # Filter rooms based on query parameters
    rooms = Room.objects.filter(status='available').select_related('category')
    
    category_id = request.GET.get('category')
    if category_id:
        rooms = rooms.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        rooms = rooms.filter(
            Q(room_number__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'rooms': rooms,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'booking/room_list.html', context)

def room_detail(request, category_id):
    category = get_object_or_404(RoomCategory, id=category_id)
    rooms = Room.objects.filter(category=category, status='available')
    
    context = {
        'category': category,
        'rooms': rooms,
    }
    return render(request, 'booking/room_detail.html', context)

@login_required
def booking_form(request):
    if request.method == 'POST':
        # Get form data
        room_id = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adults = request.POST.get('adults', 1)
        children = request.POST.get('children', 0)
        special_requests = request.POST.get('special_requests', '')
        
        # Validate dates
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            if check_in_date >= check_out_date:
                messages.error(request, 'Check-out date must be after check-in date.')
                return redirect('room_list')
            
            if check_in_date < date.today():
                messages.error(request, 'Check-in date cannot be in the past.')
                return redirect('room_list')
                
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('room_list')
        
        # Get room and calculate total
        try:
            room = Room.objects.get(id=room_id, status='available')
            nights = (check_out_date - check_in_date).days
            total_amount = room.category.base_price * nights
            
            # Store booking data in session
            request.session['booking_data'] = {
                'room_id': room.id,
                'room_number': room.room_number,
                'category_name': room.category.name,
                'check_in': check_in,
                'check_out': check_out,
                'adults': adults,
                'children': children,
                'nights': nights,
                'total_amount': str(total_amount),
                'special_requests': special_requests,
            }
            
            return redirect('booking_confirm')
            
        except Room.DoesNotExist:
            messages.error(request, 'Selected room is not available.')
            return redirect('room_list')
    
    # GET request - show booking form
    room_id = request.GET.get('room')
    room = None
    if room_id:
        room = get_object_or_404(Room, id=room_id, status='available')
    
    context = {
        'room': room,
        'min_date': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'booking/booking_form.html', context)

@login_required
def booking_confirm(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.error(request, 'Booking session expired. Please try again.')
        return redirect('room_list')
    
    context = {
        'booking_data': booking_data,
    }
    return render(request, 'booking/booking_confirm.html', context)

@login_required
def booking_success(request):
    # Get booking data from session
    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.error(request, 'Booking session expired.')
        return redirect('room_list')
    
    try:
        # Create booking
        room = Room.objects.get(id=booking_data['room_id'])
        booking = Booking.objects.create(
            customer=request.user,
            room=room,
            check_in=booking_data['check_in'],
            check_out=booking_data['check_out'],
            adults=int(booking_data['adults']),
            children=int(booking_data['children']),
            total_amount=booking_data['total_amount'],
            special_requests=booking_data['special_requests'],
            status='pending'
        )
        
        # Update room status
        room.status = 'reserved'
        room.save()
        
        # Clear session
        del request.session['booking_data']
        
        messages.success(request, f'Booking confirmed! Your booking ID is {booking.id}.')
        return render(request, 'booking/booking_success.html', {'booking': booking})
        
    except Exception as e:
        messages.error(request, f'Error creating booking: {str(e)}')
        return redirect('room_list')

@login_required
def customer_dashboard(request):
    # Get user's bookings
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    
    # Get user's reviews
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'bookings': bookings,
        'profile': profile,
    }
    return render(request, 'booking/customer_dashboard.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'booking/contact.html')
