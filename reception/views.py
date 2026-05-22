from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date
from django.http import JsonResponse
from .models import Invoice, Payment
from booking.models import Booking, Room
from accounts.models import UserProfile
from django.contrib.auth.models import User

# Helper function to check if user is reception staff
def is_reception_staff(user):
    try:
        profile = user.userprofile
        return profile.role in ['reception', 'admin']
    except UserProfile.DoesNotExist:
        return False

# Create your views here.

@login_required
@user_passes_test(is_reception_staff)
def reception_dashboard(request):
    # Get today's statistics
    today = date.today()
    
    # Today's check-ins
    today_checkins = Booking.objects.filter(check_in=today, status='confirmed').count()
    
    # Today's check-outs
    today_checkouts = Booking.objects.filter(check_out=today, status='checked_in').count()
    
    # Available rooms
    available_rooms = Room.objects.filter(status='available').count()
    
    # Pending bookings
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Recent bookings
    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]
    
    context = {
        'today_checkins': today_checkins,
        'today_checkouts': today_checkouts,
        'available_rooms': available_rooms,
        'pending_bookings': pending_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'reception/reception_dashboard.html', context)

@login_required
@user_passes_test(is_reception_staff)
def check_in(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status != 'confirmed':
        messages.error(request, 'Only confirmed bookings can be checked in.')
        return redirect('reception_dashboard')
    
    if booking.check_in > date.today():
        messages.error(request, 'Cannot check in before check-in date.')
        return redirect('reception_dashboard')
    
    # Update booking status
    booking.status = 'checked_in'
    booking.save()
    
    # Update room status
    booking.room.status = 'occupied'
    booking.room.save()
    
    messages.success(request, f'Check-in completed for Booking #{booking.id}')
    return redirect('reception_dashboard')

@login_required
@user_passes_test(is_reception_staff)
def check_out(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status != 'checked_in':
        messages.error(request, 'Only checked-in bookings can be checked out.')
        return redirect('reception_dashboard')
    
    # Update booking status
    booking.status = 'checked_out'
    booking.save()
    
    # Update room status
    booking.room.status = 'available'
    booking.room.save()
    
    messages.success(request, f'Check-out completed for Booking #{booking.id}')
    return redirect('create_invoice', booking_id=booking.id)

@login_required
@user_passes_test(is_reception_staff)
def walk_in_registration(request):
    if request.method == 'POST':
        # Get customer details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')
        
        # Get room details
        room_id = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adults = request.POST.get('adults', 1)
        children = request.POST.get('children', 0)
        
        try:
            # Create or get user
            username = email.split('@')[0] if email else f"walkin_{datetime.now().timestamp()}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            
            # Create user profile
            if created:
                UserProfile.objects.create(
                    user=user,
                    role='customer',
                    phone=phone,
                    address=address
                )
            
            # Get room and calculate total
            room = Room.objects.get(id=room_id, status='available')
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            nights = (check_out_date - check_in_date).days
            total_amount = room.category.base_price * nights
            
            # Create booking
            booking = Booking.objects.create(
                customer=user,
                room=room,
                check_in=check_in_date,
                check_out=check_out_date,
                adults=int(adults),
                children=int(children),
                total_amount=total_amount,
                status='confirmed'
            )
            
            # Update room status
            room.status = 'reserved'
            room.save()
            
            messages.success(request, f'Walk-in registration completed! Booking ID: {booking.id}')
            return redirect('reception_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')
    
    # GET request - show registration form
    available_rooms = Room.objects.filter(status='available').select_related('category')
    
    context = {
        'available_rooms': available_rooms,
        'min_date': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'reception/walk_in_registration.html', context)

@login_required
@user_passes_test(is_reception_staff)
def room_management(request):
    # Get all rooms with their current status
    rooms = Room.objects.all().select_related('category').order_by('room_number')
    
    context = {
        'rooms': rooms,
    }
    return render(request, 'reception/room_management.html', context)

@login_required
@user_passes_test(is_reception_staff)
def create_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if invoice already exists
    existing_invoice = Invoice.objects.filter(booking=booking).first()
    if existing_invoice:
        return redirect('invoice_detail', invoice_id=existing_invoice.id)
    
    if request.method == 'POST':
        # Get additional charges
        food_charges = float(request.POST.get('food_charges', 0))
        facility_charges = float(request.POST.get('facility_charges', 0))
        notes = request.POST.get('notes', '')
        
        # Calculate totals
        room_charges = booking.total_amount
        subtotal = room_charges + food_charges + facility_charges
        gst_amount = subtotal * 0.18
        total_amount = subtotal + gst_amount
        
        # Create invoice
        invoice = Invoice.objects.create(
            customer=booking.customer,
            booking=booking,
            room_charges=room_charges,
            food_charges=food_charges,
            facility_charges=facility_charges,
            subtotal=subtotal,
            gst_percentage=18.00,
            gst_amount=gst_amount,
            total_amount=total_amount,
            payment_status='pending',
            issue_date=datetime.now(),
            due_date=date.today(),
            notes=notes,
            created_by=request.user
        )
        
        messages.success(request, f'Invoice created successfully! Invoice #: {invoice.invoice_number}')
        return redirect('invoice_detail', invoice_id=invoice.id)
    
    context = {
        'booking': booking,
        'room_charges': booking.total_amount,
    }
    return render(request, 'reception/create_invoice.html', context)

@login_required
@user_passes_test(is_reception_staff)
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    context = {
        'invoice': invoice,
    }
    return render(request, 'reception/invoice_detail.html', context)

@login_required
@user_passes_test(is_reception_staff)
def all_bookings(request):
    # Get all bookings with filters
    bookings = Booking.objects.all().select_related('customer', 'room', 'room__category').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        bookings = bookings.filter(check_in__gte=date_from)
    if date_to:
        bookings = bookings.filter(check_in__lte=date_to)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'reception/all_bookings.html', context)

@login_required
@user_passes_test(is_reception_staff)
def search_booking(request):
    query = request.GET.get('q', '')
    bookings = []
    
    if query:
        # Search by booking ID, customer name, room number, or phone
        bookings = Booking.objects.filter(
            Q(id__icontains=query) |
            Q(customer__first_name__icontains=query) |
            Q(customer__last_name__icontains=query) |
            Q(customer__email__icontains=query) |
            Q(room__room_number__icontains=query) |
            Q(customer__userprofile__phone__icontains=query)
        ).select_related('customer', 'room', 'room__category').order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'query': query,
    }
    return render(request, 'reception/search_booking.html', context)

@login_required
@user_passes_test(is_reception_staff)
def invoice_success(request):
    return render(request, 'reception/invoice_success.html')
