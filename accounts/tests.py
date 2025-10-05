from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import CustomUser, UserProfile

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test cases for CustomUser model"""

    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'user'
        }

    def test_create_regular_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, 'user')
        self.assertFalse(user.is_admin())
        self.assertTrue(user.check_password('testpass123'))

    def test_create_admin_user(self):
        """Test creating an admin user"""
        admin_data = self.user_data.copy()
        admin_data['user_type'] = 'admin'
        admin_data['username'] = 'admin'

        user = User.objects.create_user(**admin_data)

        self.assertEqual(user.user_type, 'admin')
        self.assertTrue(user.is_admin())

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)

        expected_str = f"{user.username} ({user.get_user_type_display()})"
        self.assertEqual(str(user), expected_str)

    def test_is_admin_method_for_regular_user(self):
        """Test is_admin() returns False for regular user"""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_admin())

    def test_is_admin_method_for_admin_user(self):
        """Test is_admin() returns True for admin user"""
        admin_data = self.user_data.copy()
        admin_data['user_type'] = 'admin'
        admin_data['username'] = 'admin'

        user = User.objects.create_user(**admin_data)
        self.assertTrue(user.is_admin())

    def test_is_admin_method_for_superuser(self):
        """Test is_admin() returns True for superuser"""
        user = User.objects.create_superuser(
            username='superuser',
            email='super@example.com',
            password='superpass123'
        )
        self.assertTrue(user.is_admin())

    def test_user_unique_username(self):
        """Test that username must be unique"""
        User.objects.create_user(**self.user_data)

        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)

    def test_user_phone_number_optional(self):
        """Test that phone number is optional"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNone(user.phone_number)

        user.phone_number = '1234567890'
        user.save()
        self.assertEqual(user.phone_number, '1234567890')


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_user_profile(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='This is a test bio',
            location='Bangkok'
        )

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'This is a test bio')
        self.assertEqual(profile.location, 'Bangkok')

    def test_user_profile_str_representation(self):
        """Test user profile string representation"""
        profile = UserProfile.objects.create(user=self.user)

        expected_str = f"{self.user.username}'s profile"
        self.assertEqual(str(profile), expected_str)

    def test_user_profile_one_to_one_relationship(self):
        """Test one-to-one relationship between user and profile"""
        profile = UserProfile.objects.create(user=self.user)

        # Test accessing profile from user
        self.assertEqual(profile.user, self.user)

        # Test that only one profile can exist per user
        with self.assertRaises(Exception):
            UserProfile.objects.create(user=self.user)


class AuthenticationViewsTest(TestCase):
    """Test cases for authentication views"""

    def setUp(self):
        """Set up test client and user data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('accounts:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_success(self):
        """Test successful login via POST"""
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        response = self.client.post(reverse('accounts:login'), data=login_data)

        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('booking:dashboard'))

        # User should be authenticated
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = self.client.post(reverse('accounts:login'), data=login_data)

        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_redirect_authenticated_user(self):
        """Test that authenticated users are redirected from login page"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('accounts:login'))

        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('accounts:logout'))

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_logout_view_unauthenticated_user(self):
        """Test logout for unauthenticated user"""
        response = self.client.get(reverse('accounts:logout'))

        # Should still redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_view_get(self):
        """Test registration view GET request"""
        response = self.client.get(reverse('accounts:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_success(self):
        """Test successful registration via POST"""
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(reverse('accounts:register'), data=register_data)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

        # Check user was created
        user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')

    def test_register_view_post_password_mismatch(self):
        """Test registration with mismatched passwords"""
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123!@#',
            'password2': 'differentpass123!@#',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(reverse('accounts:register'), data=register_data)

        # Should stay on registration page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

        # User should not be created
        user = User.objects.filter(username='newuser').first()
        self.assertIsNone(user)

    def test_register_view_post_duplicate_username(self):
        """Test registration with existing username"""
        register_data = {
            'username': 'testuser',  # Already exists
            'email': 'another@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#',
            'first_name': 'Another',
            'last_name': 'User'
        }

        response = self.client.post(reverse('accounts:register'), data=register_data)

        # Should stay on registration page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_redirect_authenticated_user(self):
        """Test that authenticated users are redirected from register page"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('accounts:register'))

        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)

    def test_profile_view_requires_login(self):
        """Test that profile view requires login"""
        response = self.client.get(reverse('accounts:profile'))

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_view_get(self):
        """Test profile view GET request for authenticated user"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_view_post_update(self):
        """Test profile update via POST"""
        self.client.login(username='testuser', password='testpass123')

        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone_number': '0812345678'
        }

        response = self.client.post(reverse('accounts:profile'), data=update_data)

        # Should redirect to profile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile'))

        # Check user was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_dashboard_redirect_regular_user(self):
        """Test dashboard redirect for regular user"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('accounts:dashboard_redirect'))

        # Should redirect to booking dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('booking:dashboard'))

    def test_dashboard_redirect_admin_user(self):
        """Test dashboard redirect for admin user"""
        admin = User.objects.create_user(
            username='admin',
            password='admin123',
            user_type='admin',
            is_staff=True
        )

        self.client.login(username='admin', password='admin123')

        response = self.client.get(reverse('accounts:dashboard_redirect'))

        # Should redirect to admin index
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin:index'))
