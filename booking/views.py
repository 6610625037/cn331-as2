from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, date, time
from .models import Room, Booking

def test_view(request):
    """Simple test view for debugging"""
    print("DEBUG: test_view called")
    return HttpResponse("Test view working! This is a basic HTTP response.")

@login_required
def dashboard_view(request):
    """Dashboard showing overview of bookings and rooms"""
    today = date.today()

    # Get user's upcoming bookings
    user_bookings = Booking.objects.filter(
        user=request.user,
        date__gte=today,
        status__in=['confirmed', 'pending']
    ).select_related('room')[:5] if request.user.is_authenticated else []
    
    # Get available rooms today
    available_rooms = Room.objects.filter(status='open')[:6]
    
    # Statistics for admin
    context = {
        'user_bookings': user_bookings,
        'available_rooms': available_rooms,
        'today': today,
    }
    
    if request.user.is_admin():
        context.update({
            'total_rooms': Room.objects.count(),
            'total_bookings': Booking.objects.filter(date=today).count(),
            'total_users': Booking.objects.filter(date=today).values('user').distinct().count(),
        })
    
    return render(request, 'booking/dashboard.html', context)

@login_required
def room_list_view(request):
    """List all available rooms with date filter"""
    selected_date = request.GET.get('date', str(date.today()))
    
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()
    
    # Only show future dates
    if selected_date < date.today():
        selected_date = date.today()
    
    rooms = Room.objects.filter(status='open')
    
    # Add availability info for each room
    for room in rooms:
        room.available_slots = room.get_available_slots(selected_date)
        room.is_available = len(room.available_slots) > 0
    
    context = {
        'rooms': rooms,
        'selected_date': selected_date,
        'today': date.today(),
    }
    
    return render(request, 'booking/room_list.html', context)

@login_required
def room_book_view(request, room_id):
    """Book a specific room"""
    print(f"DEBUG: room_book_view called with room_id={room_id}")
    room = get_object_or_404(Room, id=room_id, status='open')
    selected_date = request.GET.get('date', str(date.today()))
    
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()
    
    if selected_date < date.today():
        messages.error(request, 'Cannot book rooms for past dates.')
        return redirect('booking:room_list')
    
    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        duration_hours = int(request.POST.get('duration_hours', 1))
        purpose = request.POST.get('purpose', '')
        expected_attendees = int(request.POST.get('expected_attendees', 1))
        special_requirements = request.POST.get('special_requirements', '')
        
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            
            # Check if room is available at this time
            if room.is_available_at_time(selected_date, start_time, duration_hours):
                booking = Booking.objects.create(
                    user=request.user,
                    room=room,
                    date=selected_date,
                    start_time=start_time,
                    duration_hours=duration_hours,
                    purpose=purpose,
                    expected_attendees=expected_attendees,
                    special_requirements=special_requirements,
                    status='confirmed'
                )
                messages.success(request, f'Successfully booked {room.name} from {start_time} for {duration_hours} hours.')
                return redirect('booking:my_bookings')
            else:
                messages.error(request, 'This time slot is not available.')
        except Exception as e:
            messages.error(request, f'Booking failed: {str(e)}')
    
    # Get available slots for the selected date
    available_slots = room.get_available_slots(selected_date)
    
    # Get existing bookings for this date to show in the UI
    existing_bookings = Booking.objects.filter(
        room=room,
        date=selected_date,
        status__in=['confirmed', 'pending']
    ).order_by('start_time')
    
    # Create booked slots info
    booked_slots = []
    for booking in existing_bookings:
        booked_slots.append({
            'start_time': booking.start_time,
            'duration': booking.duration_hours,
            'end_time': booking.end_time,
            'user': booking.user.get_full_name() or booking.user.username,
            'purpose': booking.purpose
        })
    
    context = {
        'room': room,
        'selected_date': selected_date,
        'booked_slots': booked_slots,
        'today': date.today(),
    }
    
    # FIXED: Use template instead of hardcoded HTML
    return render(request, "booking/room_book.html", context)

@login_required
def my_bookings_view(request):
    """Show user's bookings"""
    bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-date', '-start_time')
    
    context = {
        'bookings': bookings,
        'today': date.today(),
    }
    
    return render(request, 'booking/my_bookings.html', context)

@login_required
def cancel_booking_view(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.warning(request, 'This booking is already cancelled.')
    elif booking.date < date.today():
        messages.error(request, 'Cannot cancel past bookings.')
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Successfully cancelled booking for {booking.room.name} on {booking.date}.')
    
    return redirect('booking:my_bookings')
