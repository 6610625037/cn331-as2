from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from booking.models import Room
from datetime import time

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data: 1 admin + 3 users + 3 rooms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Deleting existing data...'))
            User.objects.all().delete()
            Room.objects.all().delete()

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@classroom.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created admin user: admin / admin123')
            )
        else:
            self.stdout.write(f'Admin user already exists: {admin_user.username}')

        # Create regular users
        users_data = [
            {
                'username': 'john',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+1-555-0101'
            },
            {
                'username': 'jane',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone_number': '+1-555-0102'
            },
            {
                'username': 'mike',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'phone_number': '+1-555-0103'
            }
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'phone_number': user_data.get('phone_number', ''),
                    'user_type': 'user',
                }
            )
            if created:
                user.set_password('user123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username} / user123')
                )
            else:
                self.stdout.write(f'User already exists: {user.username}')

        # Create rooms
        rooms_data = [
            {
                'code': 'R001',
                'name': 'Conference Room Alpha',
                'description': 'Large conference room with projector and whiteboard',
                'capacity': 25,
                'min_capacity': 5,
                'available_from': time(9, 0),
                'available_to': time(17, 0),
                'min_booking_hours': 1,
                'max_booking_hours': 4,
                'has_projector': True,
                'has_whiteboard': True,
                'has_computer': True,
                'has_air_conditioning': True,
                'floor_number': 2,
                'building': 'Main Building',
                'status': 'open'
            },
            {
                'code': 'R002',
                'name': 'Meeting Room Beta',
                'description': 'Medium meeting room perfect for team meetings',
                'capacity': 15,
                'min_capacity': 3,
                'available_from': time(8, 0),
                'available_to': time(18, 0),
                'min_booking_hours': 1,
                'max_booking_hours': 3,
                'has_projector': True,
                'has_whiteboard': True,
                'has_computer': False,
                'has_air_conditioning': True,
                'floor_number': 1,
                'building': 'Main Building',
                'status': 'open'
            },
            {
                'code': 'R003',
                'name': 'Training Room Gamma',
                'description': 'Large training room with advanced AV equipment',
                'capacity': 40,
                'min_capacity': 10,
                'available_from': time(9, 0),
                'available_to': time(16, 0),
                'min_booking_hours': 2,
                'max_booking_hours': 4,
                'has_projector': True,
                'has_whiteboard': True,
                'has_computer': True,
                'has_air_conditioning': True,
                'floor_number': 3,
                'building': 'Training Center',
                'status': 'open'
            }
        ]

        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                code=room_data['code'],
                defaults=room_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created room: {room.code} - {room.name}')
                )
            else:
                self.stdout.write(f'Room already exists: {room.code} - {room.name}')

        self.stdout.write(
            self.style.SUCCESS('\nSample data creation completed!')
        )
        self.stdout.write('\n=== LOGIN CREDENTIALS ===')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Users: john / user123')
        self.stdout.write('       jane / user123')
        self.stdout.write('       mike / user123')
        self.stdout.write('\n=== ROOMS CREATED ===')
        self.stdout.write('R001 - Conference Room Alpha (Capacity: 25)')
        self.stdout.write('R002 - Meeting Room Beta (Capacity: 15)')
        self.stdout.write('R003 - Training Room Gamma (Capacity: 40)')