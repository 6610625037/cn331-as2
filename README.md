### AREFANDY WAEOUSENG
### 6610625037 

# 📹 Demo Video
https://youtu.be/sxtjnc-Hc28

# 🌐 Live Application
**Cloud App URL**: https://cn331-as3.onrender.com

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

### Deployment Steps (Render)
1. Push code to GitHub deploy branch
2. Create PostgreSQL database on Render
3. Create Web Service on Render
4. Set environment variables (DATABASE_URL, DJANGO_SECRET_KEY)
5. Deploy automatically with build.sh script

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
## 📞 Support & Documentation

- **Django Documentation**: https://docs.djangoproject.com/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **TimescaleDB**: https://docs.timescale.com/

## 🧪 Testing (Assignment #4 - Testing Branch)

This branch includes comprehensive unit tests and automated testing via GitHub Actions.

### Test Coverage

The test suite includes:

#### **Booking App Tests** (`booking/tests.py`)
1. **Room Model Tests** (8 tests)
   - Room creation and validation
   - String representation
   - Unique code constraint
   - Availability checking (open/closed rooms)
   - Time-based availability
   - Overlapping booking detection
   - Available slots generation

2. **Booking Model Tests** (11 tests)
   - Booking creation and validation
   - End time calculation
   - Duration validation (min/max)
   - Capacity validation
   - Time range validation
   - Overlapping conflict detection
   - Non-overlapping bookings
   - Cancelled booking handling

3. **Booking Views Tests** (15 tests)
   - Room list view accessibility
   - Room filtering (open/closed)
   - Date filtering
   - Past date handling
   - Room booking flow (GET/POST)
   - Successful booking creation
   - Invalid booking rejection
   - My bookings view
   - Booking cancellation
   - Dashboard view

#### **Accounts App Tests** (`accounts/tests.py`)
1. **CustomUser Model Tests** (8 tests)
   - User creation (regular/admin/superuser)
   - User type validation
   - Admin permission checking
   - Unique username constraint
   - Phone number field

2. **UserProfile Model Tests** (3 tests)
   - Profile creation
   - One-to-one relationship
   - String representation

3. **Authentication Views Tests** (14 tests)
   - Login view (GET/POST)
   - Valid/invalid credentials
   - Logout functionality
   - Registration view (GET/POST)
   - Password mismatch handling
   - Duplicate username prevention
   - Profile view and updates
   - Dashboard redirects (user/admin)

### Running Tests Locally

1. **Install test dependencies**:
   ```bash
   pip install coverage
   ```

2. **Run all tests**:
   ```bash
   python manage.py test
   ```

3. **Run specific app tests**:
   ```bash
   python manage.py test booking
   python manage.py test accounts
   ```

4. **Run with coverage report**:
   ```bash
   coverage run --source='.' manage.py test
   coverage report
   coverage html
   ```

5. **View coverage report**:
   - Open `htmlcov/index.html` in your browser

### GitHub Actions Workflow

The testing branch includes automated CI/CD workflow (`.github/workflows/django-tests.yml`):

- **Triggers**: Automatically runs on push to `testing` branch
- **Python Versions**: Tests on Python 3.11 and 3.12
- **Test Steps**:
  1. Checkout code
  2. Set up Python environment
  3. Install dependencies
  4. Run migrations
  5. Execute test suite
  6. Generate coverage report
  7. Upload coverage artifacts

### Test Results

**Total Tests**: 59 tests covering:
- ✅ Models (Room, Booking, CustomUser, UserProfile)
- ✅ Views (Authentication, Booking, Dashboard)
- ✅ Forms (Login, Registration, Profile Update)
- ✅ Validation (Business logic, Permissions, Edge cases)

**Good Path Tests**: Valid user flows, successful operations
**Bad Path Tests**: Error handling, validation failures, edge cases

### Viewing Test Results

1. **Local Testing**: Run `python manage.py test` to see results in terminal
2. **GitHub Actions**: Check Actions tab in repository for workflow results
3. **Coverage Report**: Download coverage artifacts from GitHub Actions runs

---

**🎉 Your Django Classroom Booking System is ready for production use!**

**Built with ❤️ using Django Framework and Tailwind CSS**
