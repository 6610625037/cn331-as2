from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import json
import os
from datetime import datetime, time

User = get_user_model()

class Room(models.Model):
    ROOM_STATUS = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('maintenance', 'Under Maintenance'),
    )
    
    code = models.CharField(max_length=10, unique=True, help_text="Room code (e.g., R001)")
    name = models.CharField(max_length=100, help_text="Room name")
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        help_text="Maximum capacity of the room"
    )
    min_capacity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Minimum capacity required"
    )
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default='open')
    
    # Time-based settings
    available_from = models.TimeField(default=time(9, 0), help_text="Available from (e.g., 09:00)")
    available_to = models.TimeField(default=time(17, 0), help_text="Available until (e.g., 17:00)")
    min_booking_hours = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Minimum booking duration in hours"
    )
    max_booking_hours = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Maximum booking duration in hours"
    )
    
    # Additional features
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=True)
    has_computer = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=True)
    floor_number = models.IntegerField(default=1)
    building = models.CharField(max_length=50, default="Main Building")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def is_available_at_time(self, date, start_time, duration_hours):
        """Check if room is available at specific date and time"""
        if self.status != 'open':
            return False
        
        # Check if time is within available hours
        start_hour = start_time.hour
        end_hour = start_hour + duration_hours
        
        if start_hour < self.available_from.hour or end_hour > self.available_to.hour:
            return False
        
        # Check for existing bookings
        bookings = Booking.objects.filter(
            room=self,
            date=date,
            status__in=['confirmed', 'pending']
        )
        
        for booking in bookings:
            booking_start = booking.start_time.hour
            booking_end = booking_start + booking.duration_hours
            
            # Check for time overlap
            if not (end_hour <= booking_start or start_hour >= booking_end):
                return False
        
        return True
    
    def get_available_slots(self, date):
        """Get all available time slots for a specific date"""
        available_slots = []
        
        if self.status != 'open':
            return available_slots
        
        # Get all bookings for this date
        bookings = Booking.objects.filter(
            room=self,
            date=date,
            status__in=['confirmed', 'pending']
        ).order_by('start_time')
        
        # Generate all possible slots
        start_hour = self.available_from.hour
        end_hour = self.available_to.hour
        
        for hour in range(start_hour, end_hour):
            for duration in range(self.min_booking_hours, min(self.max_booking_hours + 1, end_hour - hour + 1)):
                slot_start = time(hour, 0)
                slot_end_hour = hour + duration
                
                if slot_end_hour <= end_hour:
                    is_available = True
                    
                    # Check against existing bookings
                    for booking in bookings:
                        booking_start = booking.start_time.hour
                        booking_end = booking_start + booking.duration_hours
                        
                        if not (slot_end_hour <= booking_start or hour >= booking_end):
                            is_available = False
                            break
                    
                    if is_available:
                        available_slots.append({
                            'start_time': slot_start,
                            'duration': duration,
                            'end_time': time(slot_end_hour, 0)
                        })
        
        return available_slots
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_to_json()
    
    def save_to_json(self):
        """Save room data to JSON file for admin management"""
        json_file = os.path.join(settings.JSON_DATA_DIR, 'rooms.json')
        
        # Read existing data
        rooms_data = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    rooms_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                rooms_data = []
        
        # Update or add room data
        room_dict = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'capacity': self.capacity,
            'min_capacity': self.min_capacity,
            'status': self.status,
            'available_from': self.available_from.strftime('%H:%M'),
            'available_to': self.available_to.strftime('%H:%M'),
            'min_booking_hours': self.min_booking_hours,
            'max_booking_hours': self.max_booking_hours,
            'has_projector': self.has_projector,
            'has_whiteboard': self.has_whiteboard,
            'has_computer': self.has_computer,
            'has_air_conditioning': self.has_air_conditioning,
            'floor_number': self.floor_number,
            'building': self.building,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        # Find and update existing room or append new one
        existing_index = next((i for i, room in enumerate(rooms_data) if room.get('id') == self.id), None)
        if existing_index is not None:
            rooms_data[existing_index] = room_dict
        else:
            rooms_data.append(room_dict)
        
        # Write back to file
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(rooms_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving room to JSON: {e}")

class Booking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField(help_text="Booking date")
    start_time = models.TimeField(help_text="Start time (e.g., 14:00)")
    duration_hours = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Duration in hours"
    )
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='confirmed')
    
    # Additional booking details
    purpose = models.CharField(max_length=200, blank=True, help_text="Purpose of booking")
    expected_attendees = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Expected number of attendees"
    )
    special_requirements = models.TextField(blank=True, help_text="Special requirements or notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'date', 'start_time'],
                condition=models.Q(status__in=['confirmed', 'pending']),
                name='unique_room_datetime_booking'
            )
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.room.code} on {self.date} at {self.start_time}"
    
    @property
    def end_time(self):
        """Calculate end time based on start time and duration"""
        start_hour = self.start_time.hour
        end_hour = start_hour + self.duration_hours
        return time(end_hour, self.start_time.minute)
    
    def clean(self):
        """Validate booking constraints"""
        from django.core.exceptions import ValidationError
        
        # Check if room allows this duration
        if self.duration_hours < self.room.min_booking_hours:
            raise ValidationError(f"Minimum booking duration is {self.room.min_booking_hours} hours")
        
        if self.duration_hours > self.room.max_booking_hours:
            raise ValidationError(f"Maximum booking duration is {self.room.max_booking_hours} hours")
        
        # Check if attendees fit the room
        if self.expected_attendees > self.room.capacity:
            raise ValidationError(f"Room capacity is only {self.room.capacity} people")
        
        # Check if booking time is within room available hours
        start_hour = self.start_time.hour
        end_hour = start_hour + self.duration_hours
        
        if start_hour < self.room.available_from.hour:
            raise ValidationError(f"Room is available from {self.room.available_from}")
        
        if end_hour > self.room.available_to.hour:
            raise ValidationError(f"Room is available until {self.room.available_to}")
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            room=self.room,
            date=self.date,
            status__in=['confirmed', 'pending']
        ).exclude(pk=self.pk if self.pk else None)
        
        for booking in overlapping:
            booking_start = booking.start_time.hour
            booking_end = booking_start + booking.duration_hours
            
            if not (end_hour <= booking_start or start_hour >= booking_end):
                raise ValidationError(f"Time slot conflicts with existing booking from {booking.start_time} to {booking.end_time}")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.save_to_json()
    
    def save_to_json(self):
        """Save booking data to JSON file for admin management"""
        json_file = os.path.join(settings.JSON_DATA_DIR, 'bookings.json')
        
        # Read existing data
        bookings_data = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    bookings_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                bookings_data = []
        
        # Update or add booking data
        booking_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'user_full_name': f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username,
            'room_id': self.room_id,
            'room_code': self.room.code,
            'room_name': self.room.name,
            'date': self.date.isoformat(),
            'start_time': self.start_time.strftime('%H:%M'),
            'duration_hours': self.duration_hours,
            'end_time': self.end_time.strftime('%H:%M'),
            'status': self.status,
            'purpose': self.purpose,
            'expected_attendees': self.expected_attendees,
            'special_requirements': self.special_requirements,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        # Find and update existing booking or append new one
        existing_index = next((i for i, booking in enumerate(bookings_data) if booking.get('id') == self.id), None)
        if existing_index is not None:
            bookings_data[existing_index] = booking_dict
        else:
            bookings_data.append(booking_dict)
        
        # Write back to file
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(bookings_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving booking to JSON: {e}")
