from django.contrib.auth.models import AbstractUser
from django.db import models
import json
from django.conf import settings
import os

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'Regular User'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_to_json()
    
    def save_to_json(self):
        """Save user data to JSON file for admin management"""
        json_file = os.path.join(settings.JSON_DATA_DIR, 'users.json')
        
        # Read existing data
        users_data = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                users_data = []
        
        # Update or add user data
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_type': self.user_type,
            'phone_number': self.phone_number,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
            'date_joined': self.date_joined.isoformat() if self.date_joined else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        
        # Find and update existing user or append new one
        existing_index = next((i for i, user in enumerate(users_data) if user.get('id') == self.id), None)
        if existing_index is not None:
            users_data[existing_index] = user_dict
        else:
            users_data.append(user_dict)
        
        # Write back to file
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user to JSON: {e}")

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
