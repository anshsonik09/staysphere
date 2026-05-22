from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date, time
from .models import Facility, FacilityBooking

# Create your views here.

def facilities_home(request):
    # Get all active facilities
    facilities = Facility.objects.filter(is_active=True)
    
    context = {
        'facilities': facilities,
    }
    return render(request, 'facilities/facilities_home.html', context)

def facility_detail(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id, is_active=True)
    
    # Get available time slots for today
    today = date.today()
    available_slots = get_available_time_slots(facility, today)
    
    context = {
        'facility': facility,
        'available_slots': available_slots,
        'today': today,
    }
    return render(request, 'facilities/facility_detail.html', context)

@login_required
def facility_booking(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id, is_active=True)
    
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        guests = request.POST.get('guests', 1)
        special_requests = request.POST.get('special_requests', '')
        
        # Validate inputs
        try:
            booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
            
            if booking_date_obj < date.today():
                messages.error(request, 'Booking date cannot be in the past.')
                return redirect('facility_detail', facility_id=facility.id)
            
            if start_time_obj >= end_time_obj:
                messages.error(request, 'End time must be after start time.')
                return redirect('facility_detail', facility_id=facility.id)
            
            # Check availability
            if not is_time_slot_available(facility, booking_date_obj, start_time_obj, end_time_obj):
                messages.error(request, 'Selected time slot is not available.')
                return redirect('facility_detail', facility_id=facility.id)
            
            # Calculate duration and total amount
            duration = (datetime.combine(booking_date_obj, end_time_obj) - 
                       datetime.combine(booking_date_obj, start_time_obj)).total_seconds() / 3600
            total_amount = facility.hourly_rate * duration
            
            # Create booking
            booking = FacilityBooking.objects.create(
                customer=request.user,
                facility=facility,
                date=booking_date_obj,
                start_time=start_time_obj,
                end_time=end_time_obj,
                guests=int(guests),
                total_amount=total_amount,
                special_requests=special_requests,
                status='pending'
            )
            
            messages.success(request, f'Facility booking confirmed! Booking ID: {booking.id}')
            return redirect('facility_booking_success')
            
        except ValueError:
            messages.error(request, 'Invalid date or time format.')
            return redirect('facility_detail', facility_id=facility.id)
    
    # GET request - redirect to facility detail
    return redirect('facility_detail', facility_id=facility.id)

@login_required
def facility_booking_success(request):
    return render(request, 'facilities/facility_booking_success.html')

@login_required
def facility_bookings(request):
    # Get user's facility bookings
    bookings = FacilityBooking.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'facilities/facility_bookings.html', context)

def get_available_time_slots(facility, booking_date):
    """Get available time slots for a facility on a specific date"""
    all_slots = []
    start_hour = facility.operating_hours_start.hour
    end_hour = facility.operating_hours_end.hour
    
    # Generate 1-hour slots
    for hour in range(start_hour, end_hour):
        slot_start = time(hour, 0)
        slot_end = time(hour + 1, 0)
        
        if is_time_slot_available(facility, booking_date, slot_start, slot_end):
            all_slots.append({
                'start': slot_start.strftime('%H:%M'),
                'end': slot_end.strftime('%H:%M'),
                'available': True
            })
        else:
            all_slots.append({
                'start': slot_start.strftime('%H:%M'),
                'end': slot_end.strftime('%H:%M'),
                'available': False
            })
    
    return all_slots

def is_time_slot_available(facility, booking_date, start_time, end_time):
    """Check if a time slot is available for booking"""
    # Check if the slot is within operating hours
    if start_time < facility.operating_hours_start or end_time > facility.operating_hours_end:
        return False
    
    # Check for existing bookings that overlap with the requested slot
    existing_bookings = FacilityBooking.objects.filter(
        facility=facility,
        date=booking_date,
        status__in=['pending', 'confirmed']
    ).filter(
        # Check for overlapping time slots
        Q(start_time__lt=end_time, end_time__gt=start_time)
    )
    
    # Check capacity constraint
    overlapping_bookings_count = existing_bookings.count()
    return overlapping_bookings_count < facility.capacity
