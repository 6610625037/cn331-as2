### AREFANDY WAEOUSENG
### 6610625037 

# https://youtu.be/sxtjnc-Hc28

# 🏢 Advanced Django Classroom Booking System

A comprehensive classroom booking system built with **Django Framework** and **Tailwind CSS**, featuring advanced time-based booking, TimescaleDB support, and production-ready deployment configuration.

## ✨ Key Features

### 🔐 **Advanced User Management**
- **Role-based Access Control**: Admin and Regular User roles
- **User Registration & Authentication**: Complete signup/login system
- **Admin User Management**: Promote users to admin, manage user accounts
- **Profile Management**: Update personal information and preferences

### 🏢 **Comprehensive Room Management**
- **Time-Range Booking**: Configurable time slots (e.g., 12:00-16:00 with max 4 hours)
- **Flexible Duration**: Min/Max booking hours (1-4 hours as requested)
- **Capacity Control**: Maximum and minimum capacity validation
- **Room Features**: Projector, whiteboard, computer, A/C tracking
- **Location Tracking**: Building and floor information
- **Status Management**: Open/Closed/Maintenance status

### 📅 **Smart Booking System**
- **Date Selection**: Users select date first, then see available rooms
- **Time Table Display**: Visual time slots showing booked/available periods
- **Conflict Prevention**: Automatic validation against existing bookings
- **Real-time Availability**: Dynamic availability checking
- **Purpose & Attendee Tracking**: Detailed booking information

### 👨‍💼 **Admin Dashboard Features**
- **Complete Room Management**: Add, edit, delete rooms with all parameters
- **Booking Overview**: View all bookings with user names (admin only)
- **User Management**: Promote users, manage accounts
- **Statistics Dashboard**: Room utilization, booking analytics
- **JSON Data Export**: All data automatically saved to JSON files

### 💾 **Data Management**
- **JSON Export**: Automatic export to `data/users.json`, `data/rooms.json`, `data/bookings.json`
- **Admin Data Editing**: Direct JSON file manipulation capability
- **Backup Integration**: Easy data backup and restoration

## 🚀 Technology Stack

- **Backend**: Django 5.2.6 with Python 3.13
- **Database**: SQLite (development) / PostgreSQL/TimescaleDB (production)
- **Frontend**: Tailwind CSS 3.x with responsive design
- **Authentication**: Django's built-in auth with custom user model
- **API**: Django REST Framework ready
- **Deployment**: WhiteNoise, CORS configured, production-ready

## 📋 Demo Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system management, room management, user management

### User Accounts
- **Username**: `john` | **Password**: `user123` | **Name**: John Doe
- **Username**: `jane` | **Password**: `user123` | **Name**: Jane Smith  
- **Username**: `mike` | **Password**: `user123` | **Name**: Mike Johnson

## 🏢 Sample Rooms

### R001 - Conference Room Alpha
- **Capacity**: 25 people (min: 5)
- **Hours**: 9:00 AM - 5:00 PM
- **Duration**: 1-4 hours
- **Features**: Projector ✅, Whiteboard ✅, Computer ✅, A/C ✅
- **Location**: Main Building, Floor 2

### R002 - Meeting Room Beta
- **Capacity**: 15 people (min: 3)
- **Hours**: 8:00 AM - 6:00 PM
- **Duration**: 1-3 hours
- **Features**: Projector ✅, Whiteboard ✅, A/C ✅
- **Location**: Main Building, Floor 1

### R003 - Training Room Gamma
- **Capacity**: 40 people (min: 10)
- **Hours**: 9:00 AM - 4:00 PM  
- **Duration**: 2-4 hours
- **Features**: Projector ✅, Whiteboard ✅, Computer ✅, A/C ✅
- **Location**: Training Center, Floor 3

## 🖥️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- PostgreSQL (for production)

### Quick Start

1. **Clone or access the project**
   ```bash
   cd classroom-booking-system
   ```

2. **Install dependencies**
   ```bash
   pip install django djangorestframework python-decouple psycopg2-binary pillow django-cors-headers whitenoise
   ```

3. **Set up environment (optional)**
   ```bash
   # Edit .env file for custom configuration
   # USE_SQLITE=True for development
   # Set PostgreSQL credentials for production
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create sample data**
   ```bash
   python manage.py create_sample_data
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - **Main Application**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## 🌐 Production Deployment

### Database Configuration

**For TimescaleDB/PostgreSQL:**
1. Update `.env` file:
   ```bash
   USE_SQLITE=False
   DB_NAME=your_database_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   ```

2. Install TimescaleDB extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS timescaledb;
   ```

### Cloud Deployment Ready
- **Static Files**: WhiteNoise configured
- **CORS**: Enabled for API access
- **Security**: Production security settings
- **Environment Variables**: `.env` file support
- **Database**: PostgreSQL/TimescaleDB support

### Deployment Steps
1. Set environment variables
2. Run `python manage.py migrate`
3. Run `python manage.py collectstatic`
4. Configure web server (nginx, Apache)
5. Use gunicorn/uwsgi for WSGI

## 📊 User Workflow

### 1. User Registration/Login
- New users can register with email verification
- Existing users log in with username/password
- Admin promotes users to admin role if needed

### 2. Room Booking Process
1. **Select Date**: Choose booking date (today or future)
2. **Browse Rooms**: View available rooms for selected date
3. **Check Availability**: See real-time time slots and availability
4. **Make Booking**: Select time slot, enter details, confirm booking
5. **Manage Bookings**: View, modify, or cancel existing bookings

### 3. Admin Management
1. **Room Management**: Add/edit rooms with all parameters
2. **User Management**: View users, promote to admin
3. **Booking Overview**: Monitor all bookings with user details
4. **Data Management**: Export/import JSON data

## 🔧 Advanced Features

### Time-Based Validation
- **Conflict Detection**: Prevents overlapping bookings
- **Duration Limits**: Enforces min/max booking hours per room
- **Capacity Validation**: Ensures attendee count fits room capacity
- **Time Range Checking**: Validates booking within room available hours

### JSON Data Export
All data is automatically exported to JSON files in `/data/` directory:
- `users.json`: Complete user information
- `rooms.json`: Room details and settings
- `bookings.json`: Booking history with user names

### Responsive UI
- **Mobile Optimized**: Works on all device sizes
- **Modern Design**: Beautiful Tailwind CSS styling
- **Intuitive Navigation**: Easy-to-use interface
- **Real-time Feedback**: Instant validation and updates

## 📁 Project Structure

```
classroom-booking-system/
├── accounts/                 # User management app
│   ├── models.py            # Custom user model
│   ├── views.py             # Authentication views
│   ├── forms.py             # Registration/login forms
│   └── admin.py             # User admin interface
├── booking/                 # Room booking app
│   ├── models.py            # Room and Booking models
│   ├── views.py             # Booking views
│   ├── admin.py             # Room admin interface
│   └── management/commands/ # Management commands
├── templates/               # HTML templates
│   ├── base.html           # Base template with Tailwind
│   ├── accounts/           # Authentication templates
│   └── booking/            # Booking templates
├── static/                 # Static files
├── data/                   # JSON data exports
├── .env                    # Environment configuration
└── requirements.txt        # Python dependencies
```

## 🔒 Security Features

- **CSRF Protection**: All forms protected
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **User Authentication**: Secure password hashing
- **Permission Checking**: Role-based access control
- **Input Validation**: Server-side validation

## 📈 Scalability & Performance

- **Database Optimization**: Efficient queries with select_related
- **Caching Ready**: Django caching framework support
- **Static Files**: WhiteNoise for efficient static serving
- **Production Settings**: Optimized for deployment
- **TimescaleDB Support**: Time-series data optimization

## 🤝 Contributing

This system is designed to be easily extensible:

1. **Add New Features**: Create new Django apps
2. **Extend Models**: Add fields to existing models
3. **Custom Views**: Add specialized booking views
4. **API Integration**: Use Django REST Framework
5. **Frontend Enhancement**: Customize Tailwind components

## 📞 Support & Documentation

- **Django Documentation**: https://docs.djangoproject.com/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **TimescaleDB**: https://docs.timescale.com/

---

**🎉 Your Django Classroom Booking System is ready for production use!**

**Built with ❤️ using Django Framework and Tailwind CSS**