from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import CustomUser, UserProfile
import csv
import json
from datetime import datetime

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'get_full_name', 'user_type', 'is_active', 
        'last_login_formatted', 'date_joined_formatted', 'booking_count', 'action_buttons'
    )
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)
    list_per_page = 20
    list_editable = ('is_active',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'profile_picture'),
            'classes': ('wide',)
        }),
        ('Account Statistics', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse', 'wide'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email'),
            'classes': ('wide',)
        }),
        ('Additional Information', {
            'fields': ('user_type', 'phone_number'),
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    inlines = [UserProfileInline]
    
    actions = [
        'make_admin', 'make_user', 'activate_users', 'deactivate_users',
        'reset_passwords', 'send_welcome_email', 'export_users_csv', 'export_users_json'
    ]
    
    # Custom display methods
    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username
    get_full_name.short_description = 'Full Name'
    
    def last_login_formatted(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%Y-%m-%d %H:%M')
        return 'Never'
    last_login_formatted.short_description = 'Last Login'
    last_login_formatted.admin_order_field = 'last_login'
    
    def date_joined_formatted(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d %H:%M')
    date_joined_formatted.short_description = 'Date Joined'
    date_joined_formatted.admin_order_field = 'date_joined'
    
    def booking_count(self, obj):
        count = obj.bookings.count()
        if count > 0:
            return format_html(
                '<a href="/admin/booking/booking/?user__id__exact={}" style="color: #007cba;">{}</a>',
                obj.id, count
            )
        return count
    booking_count.short_description = 'Bookings'
    
    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Reset Password</a>&nbsp;'
            '<a class="button" href="{}">View Bookings</a>',
            reverse('admin:reset_user_password', args=[obj.pk]),
            f'/admin/booking/booking/?user__id__exact={obj.id}'
        )
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True
    
    # Custom URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/reset-password/', 
                 self.admin_site.admin_view(self.reset_password_view), 
                 name='reset_user_password'),
            path('bulk-operations/', 
                 self.admin_site.admin_view(self.bulk_operations_view), 
                 name='user_bulk_operations'),
            path('user-analytics/', 
                 self.admin_site.admin_view(self.user_analytics_view), 
                 name='user_analytics'),
        ]
        return custom_urls + urls
    
    # Custom views
    def reset_password_view(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Password for {user.username} has been reset successfully.')
                return redirect('admin:accounts_customuser_changelist')
        else:
            form = AdminPasswordChangeForm(user)
        
        context = {
            'form': form,
            'user': user,
            'title': f'Reset Password for {user.username}',
        }
        return render(request, 'admin/accounts/reset_password.html', context)
    
    def bulk_operations_view(self, request):
        users = CustomUser.objects.all()
        context = {
            'users': users,
            'title': 'Bulk User Operations',
        }
        return render(request, 'admin/accounts/bulk_operations.html', context)
    
    def user_analytics_view(self, request):
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        admin_users = CustomUser.objects.filter(user_type='admin').count()
        recent_users = CustomUser.objects.order_by('-date_joined')[:10]
        
        context = {
            'total_users': total_users,
            'active_users': active_users,
            'admin_users': admin_users,
            'inactive_users': total_users - active_users,
            'recent_users': recent_users,
            'title': 'User Analytics',
        }
        return render(request, 'admin/accounts/user_analytics.html', context)
    
    # Action methods
    def make_admin(self, request, queryset):
        updated = queryset.update(user_type='admin', is_staff=True)
        self.message_user(request, f'{updated} users were successfully promoted to admin.')
    make_admin.short_description = "🔧 Promote selected users to admin"
    
    def make_user(self, request, queryset):
        updated = queryset.filter(is_superuser=False).update(user_type='user', is_staff=False)
        self.message_user(request, f'{updated} users were successfully demoted to regular users.')
    make_user.short_description = "👤 Demote selected users to regular users"
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "✅ Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.filter(is_superuser=False).update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "❌ Deactivate selected users"
    
    def reset_passwords(self, request, queryset):
        count = 0
        for user in queryset:
            # Generate a temporary password
            temp_password = f"temp_{user.username}_{datetime.now().strftime('%Y%m%d')}"
            user.set_password(temp_password)
            user.save()
            count += 1
        self.message_user(request, f'{count} passwords were reset. Temporary passwords follow the pattern: temp_username_YYYYMMDD')
    reset_passwords.short_description = "🔑 Reset passwords for selected users"
    
    def send_welcome_email(self, request, queryset):
        # Placeholder for email functionality
        count = queryset.count()
        self.message_user(request, f'Welcome emails would be sent to {count} users. (Email system not configured)')
    send_welcome_email.short_description = "📧 Send welcome email"
    
    def export_users_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'User Type', 'Is Active', 'Date Joined', 'Last Login'])
        
        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.user_type,
                user.is_active,
                user.date_joined,
                user.last_login
            ])
        
        return response
    export_users_csv.short_description = "📊 Export selected users to CSV"
    
    def export_users_json(self, request, queryset):
        users_data = []
        for user in queryset:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'phone_number': user.phone_number,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                'last_login': user.last_login.isoformat() if user.last_login else None,
            })
        
        response = HttpResponse(
            json.dumps(users_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="users.json"'
        return response
    export_users_json.short_description = "📋 Export selected users to JSON"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'location', 'created_at')
    list_filter = ('birth_date', 'location')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'location', 'bio')
    readonly_fields = ('user',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def created_at(self, obj):
        return obj.user.created_at.strftime('%Y-%m-%d %H:%M')
    created_at.short_description = 'Profile Created'
    created_at.admin_order_field = 'user__created_at'
