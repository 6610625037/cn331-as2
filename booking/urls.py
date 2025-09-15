from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('test/', views.test_view, name='test'),  # Debug test URL
    path('', views.dashboard_view, name='dashboard'),
    path('rooms/', views.room_list_view, name='room_list'),
    path('rooms/<int:room_id>/book/', views.room_book_view, name='room_book'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
]