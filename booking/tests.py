from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date, time, timedelta
from .models import Room, Booking

User = get_user_model()


class RoomModelTest(TestCase):
    """Test cases for Room model"""

    def setUp(self):
        """Set up test data"""
        self.room = Room.objects.create(
            code='R001',
            name='Conference Room A',
            description='A large conference room',
            capacity=50,
            min_capacity=5,
            status='open',
            available_from=time(9, 0),
            available_to=time(17, 0),
            min_booking_hours=1,
            max_booking_hours=4,
            has_projector=True,
            has_whiteboard=True,
            floor_number=1,
            building='Main Building'
        )

    def test_room_creation(self):
        """Test that room is created correctly"""
        self.assertEqual(self.room.code, 'R001')
        self.assertEqual(self.room.name, 'Conference Room A')
        self.assertEqual(self.room.capacity, 50)
        self.assertEqual(self.room.status, 'open')

    def test_room_str_representation(self):
        """Test room string representation"""
        self.assertEqual(str(self.room), 'R001 - Conference Room A')

    def test_room_unique_code(self):
        """Test that room code must be unique"""
        with self.assertRaises(Exception):
            Room.objects.create(
                code='R001',  # Duplicate code
                name='Another Room',
                capacity=30
            )

    def test_is_available_at_time_open_room(self):
        """Test room availability for open room with no bookings"""
        test_date = date.today() + timedelta(days=1)
        start_time = time(10, 0)
        duration = 2

        self.assertTrue(self.room.is_available_at_time(test_date, start_time, duration))

    def test_is_available_at_time_closed_room(self):
        """Test room availability for closed room"""
        self.room.status = 'closed'
        self.room.save()

        test_date = date.today() + timedelta(days=1)
        start_time = time(10, 0)
        duration = 2

        self.assertFalse(self.room.is_available_at_time(test_date, start_time, duration))

    def test_is_available_at_time_outside_hours(self):
        """Test room availability outside available hours"""
        test_date = date.today() + timedelta(days=1)
        start_time = time(8, 0)  # Before available_from (9:00)
        duration = 2

        self.assertFalse(self.room.is_available_at_time(test_date, start_time, duration))

    def test_is_available_at_time_with_existing_booking(self):
        """Test room availability when there's an existing booking"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        test_date = date.today() + timedelta(days=1)

        # Create existing booking from 10:00 to 12:00
        Booking.objects.create(
            user=user,
            room=self.room,
            date=test_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        # Try to book overlapping time (11:00 to 13:00)
        self.assertFalse(self.room.is_available_at_time(test_date, time(11, 0), 2))

        # Try to book non-overlapping time (13:00 to 15:00)
        self.assertTrue(self.room.is_available_at_time(test_date, time(13, 0), 2))

    def test_get_available_slots(self):
        """Test getting available slots for a date"""
        test_date = date.today() + timedelta(days=1)
        slots = self.room.get_available_slots(test_date)

        self.assertIsInstance(slots, list)
        self.assertGreater(len(slots), 0)

        # Check slot structure
        if slots:
            slot = slots[0]
            self.assertIn('start_time', slot)
            self.assertIn('duration', slot)
            self.assertIn('end_time', slot)


class BookingModelTest(TestCase):
    """Test cases for Booking model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

        self.room = Room.objects.create(
            code='R001',
            name='Test Room',
            capacity=30,
            min_capacity=1,
            status='open',
            available_from=time(9, 0),
            available_to=time(17, 0),
            min_booking_hours=1,
            max_booking_hours=4
        )

        self.booking_date = date.today() + timedelta(days=1)

    def test_booking_creation(self):
        """Test that booking is created correctly"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            purpose='Team Meeting',
            expected_attendees=10,
            status='confirmed'
        )

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.duration_hours, 2)
        self.assertEqual(booking.status, 'confirmed')

    def test_booking_str_representation(self):
        """Test booking string representation"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10
        )

        expected_str = f"testuser - R001 on {self.booking_date} at 10:00:00"
        self.assertEqual(str(booking), expected_str)

    def test_booking_end_time_property(self):
        """Test end_time property calculation"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10
        )

        self.assertEqual(booking.end_time, time(12, 0))

    def test_booking_duration_below_minimum(self):
        """Test booking validation for duration below minimum"""
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                room=self.room,
                date=self.booking_date,
                start_time=time(10, 0),
                duration_hours=0,  # Below minimum
                expected_attendees=10
            )
            booking.clean()

    def test_booking_duration_above_maximum(self):
        """Test booking validation for duration above maximum"""
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                room=self.room,
                date=self.booking_date,
                start_time=time(10, 0),
                duration_hours=5,  # Above room's max (4)
                expected_attendees=10
            )
            booking.clean()

    def test_booking_exceeds_room_capacity(self):
        """Test booking validation for exceeding room capacity"""
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                room=self.room,
                date=self.booking_date,
                start_time=time(10, 0),
                duration_hours=2,
                expected_attendees=50  # Exceeds room capacity (30)
            )
            booking.clean()

    def test_booking_outside_available_hours(self):
        """Test booking validation for time outside available hours"""
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                room=self.room,
                date=self.booking_date,
                start_time=time(8, 0),  # Before available_from (9:00)
                duration_hours=2,
                expected_attendees=10
            )
            booking.clean()

    def test_booking_overlapping_conflict(self):
        """Test booking validation for overlapping bookings"""
        # Create first booking
        Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        # Try to create overlapping booking
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                room=self.room,
                date=self.booking_date,
                start_time=time(11, 0),  # Overlaps with 10:00-12:00
                duration_hours=2,
                expected_attendees=10,
                status='confirmed'
            )
            booking.clean()

    def test_booking_non_overlapping_allowed(self):
        """Test that non-overlapping bookings are allowed"""
        # Create first booking
        Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        # Create non-overlapping booking (should succeed)
        booking2 = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(13, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        self.assertEqual(booking2.start_time, time(13, 0))

    def test_cancelled_booking_no_conflict(self):
        """Test that cancelled bookings don't cause conflicts"""
        # Create cancelled booking
        Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='cancelled'
        )

        # Create booking at same time (should succeed)
        booking2 = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.booking_date,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        self.assertEqual(booking2.start_time, time(10, 0))


class BookingViewsTest(TestCase):
    """Test cases for booking views"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            user_type='admin',
            is_staff=True
        )

        self.room = Room.objects.create(
            code='R001',
            name='Test Room',
            capacity=30,
            status='open',
            available_from=time(9, 0),
            available_to=time(17, 0),
            min_booking_hours=1,
            max_booking_hours=4
        )

    def test_room_list_view_accessible(self):
        """Test that room list view is accessible"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:room_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/room_list.html')

    def test_room_list_view_shows_open_rooms(self):
        """Test that room list view shows only open rooms"""
        self.client.login(username='testuser', password='testpass123')

        # Create closed room
        Room.objects.create(
            code='R002',
            name='Closed Room',
            capacity=20,
            status='closed'
        )

        response = self.client.get(reverse('booking:room_list'))
        self.assertEqual(response.status_code, 200)

        # Only open room should be displayed
        rooms = response.context['rooms']
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].code, 'R001')

    def test_room_list_view_date_filter(self):
        """Test room list view with date filter"""
        self.client.login(username='testuser', password='testpass123')
        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('booking:room_list'), {'date': tomorrow})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_date'], date.today() + timedelta(days=1))

    def test_room_list_view_past_date_redirects_to_today(self):
        """Test that past dates are redirected to today"""
        self.client.login(username='testuser', password='testpass123')
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('booking:room_list'), {'date': yesterday})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_date'], date.today())

    def test_room_book_view_get(self):
        """Test room booking view GET request"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(
            reverse('booking:room_book', kwargs={'room_id': self.room.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/room_book.html')
        self.assertEqual(response.context['room'], self.room)

    def test_room_book_view_post_success(self):
        """Test successful room booking via POST"""
        self.client.login(username='testuser', password='testpass123')

        tomorrow = date.today() + timedelta(days=1)
        booking_data = {
            'start_time': '10:00',
            'duration_hours': 2,
            'purpose': 'Team Meeting',
            'expected_attendees': 15,
            'special_requirements': ''
        }

        response = self.client.post(
            reverse('booking:room_book', kwargs={'room_id': self.room.id}) + f'?date={tomorrow}',
            data=booking_data
        )

        # Should redirect to my_bookings
        self.assertEqual(response.status_code, 302)

        # Check booking was created
        booking = Booking.objects.filter(user=self.user, room=self.room).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.purpose, 'Team Meeting')
        self.assertEqual(booking.expected_attendees, 15)

    def test_room_book_view_post_past_date_fails(self):
        """Test booking past date fails"""
        self.client.login(username='testuser', password='testpass123')

        yesterday = date.today() - timedelta(days=1)
        response = self.client.get(
            reverse('booking:room_book', kwargs={'room_id': self.room.id}) + f'?date={yesterday}'
        )

        # Should redirect to room_list
        self.assertEqual(response.status_code, 302)

    def test_room_book_view_post_unavailable_slot_fails(self):
        """Test booking unavailable time slot fails"""
        self.client.login(username='testuser', password='testpass123')

        tomorrow = date.today() + timedelta(days=1)

        # Create existing booking
        Booking.objects.create(
            user=self.user,
            room=self.room,
            date=tomorrow,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        # Try to book overlapping slot
        booking_data = {
            'start_time': '11:00',  # Overlaps with 10:00-12:00
            'duration_hours': 2,
            'purpose': 'Another Meeting',
            'expected_attendees': 15
        }

        response = self.client.post(
            reverse('booking:room_book', kwargs={'room_id': self.room.id}) + f'?date={tomorrow}',
            data=booking_data
        )

        # Should stay on same page with error
        self.assertEqual(response.status_code, 200)

    def test_my_bookings_view_requires_login(self):
        """Test that my_bookings view requires login"""
        response = self.client.get(reverse('booking:my_bookings'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_my_bookings_view_shows_user_bookings(self):
        """Test that my_bookings view shows only user's bookings"""
        self.client.login(username='testuser', password='testpass123')

        # Create booking for logged in user
        tomorrow = date.today() + timedelta(days=1)
        booking1 = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=tomorrow,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10
        )

        # Create booking for another user
        other_user = User.objects.create_user(username='other', password='pass123')
        booking2 = Booking.objects.create(
            user=other_user,
            room=self.room,
            date=tomorrow,
            start_time=time(14, 0),
            duration_hours=2,
            expected_attendees=10
        )

        response = self.client.get(reverse('booking:my_bookings'))

        bookings = response.context['bookings']
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0].id, booking1.id)

    def test_cancel_booking_view_success(self):
        """Test successful booking cancellation"""
        self.client.login(username='testuser', password='testpass123')

        tomorrow = date.today() + timedelta(days=1)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=tomorrow,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        response = self.client.get(
            reverse('booking:cancel_booking', kwargs={'booking_id': booking.id})
        )

        # Should redirect to my_bookings
        self.assertEqual(response.status_code, 302)

        # Check booking is cancelled
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_cancel_booking_view_past_booking_fails(self):
        """Test cancelling past booking fails"""
        self.client.login(username='testuser', password='testpass123')

        yesterday = date.today() - timedelta(days=1)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=yesterday,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='confirmed'
        )

        response = self.client.get(
            reverse('booking:cancel_booking', kwargs={'booking_id': booking.id})
        )

        # Should redirect but booking should not be cancelled
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'confirmed')

    def test_cancel_already_cancelled_booking(self):
        """Test cancelling already cancelled booking"""
        self.client.login(username='testuser', password='testpass123')

        tomorrow = date.today() + timedelta(days=1)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=tomorrow,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10,
            status='cancelled'
        )

        response = self.client.get(
            reverse('booking:cancel_booking', kwargs={'booking_id': booking.id})
        )

        # Should redirect
        self.assertEqual(response.status_code, 302)

        # Booking should remain cancelled
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_dashboard_view_accessible(self):
        """Test dashboard view is accessible"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/dashboard.html')

    def test_dashboard_view_shows_upcoming_bookings(self):
        """Test dashboard shows upcoming bookings"""
        self.client.login(username='testuser', password='testpass123')

        tomorrow = date.today() + timedelta(days=1)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=tomorrow,
            start_time=time(10, 0),
            duration_hours=2,
            expected_attendees=10
        )

        response = self.client.get(reverse('booking:dashboard'))

        user_bookings = response.context['user_bookings']
        self.assertEqual(len(user_bookings), 1)
        self.assertEqual(user_bookings[0].id, booking.id)
