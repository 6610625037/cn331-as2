"""
Classroom Booking System Configuration File
===========================================

This file contains all configurable settings for the classroom booking system.
Modify these settings to customize the system behavior without changing core code.
"""

from datetime import datetime


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Database Backend Selection
DATABASE_BACKEND = 'sqlite'  # Options: 'sqlite', 'postgresql', 'timescaledb'

# SQLite Configuration (for development)
SQLITE_CONFIG = {
    'enabled': True,
    'database_path': 'db.sqlite3',  # Relative to project root
}

# PostgreSQL/TimescaleDB Configuration (for production)
POSTGRESQL_CONFIG = {
    'enabled': False,
    'database_name': 'classroom_booking',
    'username': 'postgres',
    'password': 'your_password_here',
    'host': 'localhost',
    'port': '5432',
    'use_timescaledb': True,  # Enable TimescaleDB extensions
    'connection_timeout': 60,
    'max_connections': 20,
}

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Basic Application Settings
APP_CONFIG = {
    'app_name': 'Classroom Booking System',
    'app_version': '2.0.0',
    'app_description': 'Advanced Django-based classroom booking system',
    'admin_email': 'admin@classroom.local',
    'support_email': 'support@classroom.local',
    'timezone': 'Asia/Bangkok',
    'language_code': 'en-us',
}

# Security Settings
SECURITY_CONFIG = {
    'debug_mode': True,  # Set to False in production
    'allowed_hosts': ['localhost', '127.0.0.1', '*'],
    'secret_key_env_var': 'SECRET_KEY',  # Environment variable name
    'session_cookie_age': 86400,  # 24 hours in seconds
    'csrf_protection': True,
    'secure_ssl_redirect': False,  # Set to True in production with HTTPS
    'session_cookie_secure': False,  # Set to True in production with HTTPS
}

# =============================================================================
# BOOKING SYSTEM CONFIGURATION
# =============================================================================

# Room Booking Settings
BOOKING_CONFIG = {
    'default_booking_duration': 1,  # hours
    'min_booking_duration': 1,      # hours
    'max_booking_duration': 4,      # hours
    'advance_booking_days': 30,     # How many days in advance users can book
    'booking_cancellation_hours': 2, # Minimum hours before booking to cancel
    'default_room_capacity': 20,
    'max_room_capacity': 200,
    'min_room_capacity': 1,
}

# Time Slot Configuration
TIME_SLOT_CONFIG = {
    'default_start_time': '09:00',
    'default_end_time': '17:00',
    'slot_duration': 60,  # minutes
    'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    'weekend_booking': False,
    'holiday_booking': False,
}

# Room Features Configuration
ROOM_FEATURES = {
    'available_features': [
        'projector',
        'whiteboard',
        'computer',
        'air_conditioning',
        'microphone',
        'video_conference',
        'smart_board',
        'sound_system'
    ],
    'required_features': ['whiteboard'],  # Features all rooms must have
    'premium_features': ['video_conference', 'smart_board'],  # Special features
}

# =============================================================================
# USER MANAGEMENT CONFIGURATION
# =============================================================================

# User Account Settings
USER_CONFIG = {
    'allow_registration': True,
    'require_email_verification': False,
    'default_user_role': 'user',  # 'user' or 'admin'
    'password_min_length': 8,
    'require_strong_password': True,
    'max_login_attempts': 5,
    'lockout_duration': 300,  # 5 minutes in seconds
}

# User Profile Settings
PROFILE_CONFIG = {
    'required_fields': ['first_name', 'last_name', 'email'],
    'optional_fields': ['phone_number', 'department', 'employee_id'],
    'allow_profile_picture': True,
    'max_profile_picture_size': 5,  # MB
}

# Admin Permissions
ADMIN_CONFIG = {
    'super_admin_permissions': [
        'manage_users',
        'manage_rooms',
        'manage_bookings',
        'view_analytics',
        'system_settings',
        'data_export',
        'user_impersonation'
    ],
    'regular_admin_permissions': [
        'manage_rooms',
        'manage_bookings',
        'view_analytics'
    ],
}

# =============================================================================
# UI/UX CONFIGURATION
# =============================================================================

# Theme and Styling
UI_CONFIG = {
    'theme': 'modern',  # 'modern', 'classic', 'minimal'
    'primary_color': '#3b82f6',  # Blue
    'secondary_color': '#1f2937',  # Dark gray
    'success_color': '#10b981',  # Green
    'warning_color': '#f59e0b',  # Orange
    'error_color': '#ef4444',   # Red
    'font_family': 'Inter, sans-serif',
    'enable_dark_mode': True,
    'default_dark_mode': False,
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'show_statistics': True,
    'show_recent_bookings': True,
    'show_available_rooms': True,
    'max_recent_items': 5,
    'refresh_interval': 30,  # seconds
    'enable_notifications': True,
}

# =============================================================================
# DATA MANAGEMENT CONFIGURATION
# =============================================================================

# JSON Export Settings
DATA_EXPORT_CONFIG = {
    'enable_json_export': True,
    'export_directory': 'data',
    'auto_export': True,
    'export_format': 'json',  # 'json', 'csv', 'xlsx'
    'backup_on_change': True,
    'max_backup_files': 10,
    'compress_exports': False,
}

# File Storage Settings
STORAGE_CONFIG = {
    'media_root': 'media',
    'static_root': 'staticfiles',
    'upload_max_size': 10,  # MB
    'allowed_file_types': ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'],
}

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# Email Settings (for notifications)
EMAIL_CONFIG = {
    'enabled': False,
    'backend': 'smtp',  # 'smtp', 'sendmail', 'console'
    'smtp_host': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_use_tls': True,
    'smtp_username': 'your_email@gmail.com',
    'smtp_password': 'your_app_password',
    'default_from_email': 'noreply@classroom.local',
}

# Notification Settings
NOTIFICATION_CONFIG = {
    'send_booking_confirmation': True,
    'send_booking_reminder': True,
    'send_cancellation_notice': True,
    'reminder_hours_before': [24, 2],  # Send reminders 24h and 2h before
    'admin_notifications': True,
}

# =============================================================================
# API CONFIGURATION
# =============================================================================

# REST API Settings
API_CONFIG = {
    'enabled': True,
    'version': 'v1',
    'base_url': '/api/',
    'authentication': ['session', 'token'],
    'permission_classes': ['IsAuthenticated'],
    'pagination_size': 20,
    'max_pagination_size': 100,
    'throttling': {
        'anon_rate': '100/hour',
        'user_rate': '1000/hour',
        'admin_rate': 'unlimited'
    }
}

# CORS Settings
CORS_CONFIG = {
    'enabled': True,
    'allow_all_origins': True,  # Set to False in production
    'allowed_origins': [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'https://yourdomain.com'
    ],
    'allow_credentials': True,
    'allowed_methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
}

# =============================================================================
# MONITORING AND LOGGING
# =============================================================================

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'log_to_file': True,
    'log_file': 'logs/classroom_booking.log',
    'max_file_size': 10,  # MB
    'backup_count': 5,
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_requests': True,
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'enabled': True,
    'track_user_activity': True,
    'track_booking_patterns': True,
    'generate_reports': True,
    'report_frequency': 'weekly',  # 'daily', 'weekly', 'monthly'
    'retention_days': 365,
}

# =============================================================================
# DEPLOYMENT CONFIGURATION
# =============================================================================

# Production Settings
PRODUCTION_CONFIG = {
    'environment': 'development',  # 'development', 'staging', 'production'
    'use_cdn': False,
    'cdn_url': 'https://cdn.example.com',
    'compress_static_files': True,
    'enable_caching': True,
    'cache_backend': 'redis',  # 'redis', 'memcached', 'database'
    'cache_timeout': 300,  # 5 minutes
}

# Docker Configuration
DOCKER_CONFIG = {
    'enabled': False,
    'use_docker_compose': True,
    'postgres_service': 'db',
    'redis_service': 'redis',
    'web_port': 8000,
}

# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

# Development Tools
DEVELOPMENT_CONFIG = {
    'debug_toolbar': True,
    'shell_plus': True,
    'runserver_plus': True,
    'show_sql_queries': False,
    'auto_reload': True,
    'collect_static_on_start': False,
}

# Testing Configuration
TESTING_CONFIG = {
    'test_database': 'test_classroom_booking',
    'use_test_fixtures': True,
    'create_test_data': True,
    'run_migrations_for_tests': True,
    'parallel_tests': False,
}

# =============================================================================
# FEATURE FLAGS
# =============================================================================

# Feature Toggle System
FEATURE_FLAGS = {
    'booking_system': True,
    'user_registration': True,
    'email_notifications': False,
    'advanced_analytics': True,
    'api_endpoints': True,
    'mobile_app_support': False,
    'multi_language': False,
    'calendar_integration': False,
    'payment_system': False,
    'reporting_system': True,
}

# Experimental Features
EXPERIMENTAL_FEATURES = {
    'ai_room_suggestions': False,
    'voice_bookings': False,
    'qr_code_checkin': False,
    'iot_integration': False,
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_database_config():
    """Get the active database configuration"""
    if DATABASE_BACKEND == 'sqlite':
        return SQLITE_CONFIG
    elif DATABASE_BACKEND in ['postgresql', 'timescaledb']:
        return POSTGRESQL_CONFIG
    else:
        raise ValueError(f"Unsupported database backend: {DATABASE_BACKEND}")

def is_feature_enabled(feature_name):
    """Check if a feature is enabled"""
    return FEATURE_FLAGS.get(feature_name, False) or EXPERIMENTAL_FEATURES.get(feature_name, False)

def get_time_slots():
    """Generate time slots based on configuration"""
    from datetime import datetime, timedelta
    
    start_time = datetime.strptime(TIME_SLOT_CONFIG['default_start_time'], '%H:%M')
    end_time = datetime.strptime(TIME_SLOT_CONFIG['default_end_time'], '%H:%M')
    slot_duration = timedelta(minutes=TIME_SLOT_CONFIG['slot_duration'])
    
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime('%H:%M'))
        current_time += slot_duration
    
    return slots

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Validate database configuration
    if DATABASE_BACKEND not in ['sqlite', 'postgresql', 'timescaledb']:
        errors.append(f"Invalid DATABASE_BACKEND: {DATABASE_BACKEND}")
    
    # Validate booking configuration
    if BOOKING_CONFIG['min_booking_duration'] > BOOKING_CONFIG['max_booking_duration']:
        errors.append("min_booking_duration cannot be greater than max_booking_duration")
    
    # Validate time slot configuration
    try:
        datetime.strptime(TIME_SLOT_CONFIG['default_start_time'], '%H:%M')
        datetime.strptime(TIME_SLOT_CONFIG['default_end_time'], '%H:%M')
    except ValueError:
        errors.append("Invalid time format in TIME_SLOT_CONFIG")
    
    return errors

# Run validation on import
_config_errors = validate_config()
if _config_errors:
    print("Configuration Errors:")
    for error in _config_errors:
        print(f"  - {error}")

# Export commonly used configurations
__all__ = [
    'DATABASE_BACKEND', 'APP_CONFIG', 'BOOKING_CONFIG', 'USER_CONFIG',
    'UI_CONFIG', 'DATA_EXPORT_CONFIG', 'FEATURE_FLAGS',
    'get_database_config', 'is_feature_enabled', 'get_time_slots'
]