from django.contrib import admin
from django.utils.html import format_html
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'capacity', 'status', 'available_time_range', 'booking_duration_range', 'features_summary', 'created_at')
    list_filter = ('status', 'building', 'floor_number', 'has_projector', 'has_computer', 'has_air_conditioning')
    search_fields = ('code', 'name', 'description', 'building')
    ordering = ('code',)
    list_editable = ('status',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'status')
        }),
        ('Capacity Settings', {
            'fields': ('capacity', 'min_capacity')
        }),
        ('Time Settings', {
            'fields': ('available_from', 'available_to', 'min_booking_hours', 'max_booking_hours')
        }),
        ('Location', {
            'fields': ('building', 'floor_number')
        }),
        ('Features', {
            'fields': ('has_projector', 'has_whiteboard', 'has_computer', 'has_air_conditioning')
        }),
    )
    
    def available_time_range(self, obj):
        return f"{obj.available_from} - {obj.available_to}"
    available_time_range.short_description = "Available Time"
    
    def booking_duration_range(self, obj):
        return f"{obj.min_booking_hours} - {obj.max_booking_hours} hours"
    booking_duration_range.short_description = "Booking Duration"
    
    def features_summary(self, obj):
        features = []
        if obj.has_projector: features.append("📽️")
        if obj.has_whiteboard: features.append("📝")
        if obj.has_computer: features.append("💻")
        if obj.has_air_conditioning: features.append("❄️")
        return "".join(features) if features else "-"
    features_summary.short_description = "Features"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date', 'time_slot', 'duration_hours', 'expected_attendees', 'status', 'created_at')
    list_filter = ('status', 'date', 'room__building', 'duration_hours')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'room__code', 'room__name', 'purpose')
    ordering = ('-created_at',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'room', 'date', 'start_time', 'duration_hours', 'status')
        }),
        ('Details', {
            'fields': ('purpose', 'expected_attendees', 'special_requirements')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['confirm_bookings', 'cancel_bookings', 'complete_bookings']
    
    def time_slot(self, obj):
        return f"{obj.start_time} - {obj.end_time}"
    time_slot.short_description = "Time Slot"
    
    def confirm_bookings(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings were successfully confirmed.')
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings were successfully cancelled.')
    cancel_bookings.short_description = "Cancel selected bookings"
    
    def complete_bookings(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} bookings were successfully completed.')
    complete_bookings.short_description = "Mark selected bookings as completed"
