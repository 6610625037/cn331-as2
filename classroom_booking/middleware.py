from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware that requires user to be authenticated to access most pages
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        public_urls = [
            reverse('accounts:login'),
            reverse('accounts:register'),
            reverse('accounts:logout'),
            '/admin/',
        ]
        
        # Allow access to static files, admin, and public URLs
        if (request.path.startswith('/static/') or 
            request.path.startswith('/media/') or
            request.path.startswith('/admin/') or
            request.path in public_urls or
            request.path == '/'):  # Allow root redirect
            return self.get_response(request)
        
        # Redirect unauthenticated users to login
        if not request.user.is_authenticated and request.path != reverse('accounts:login'):
            return redirect('accounts:login')
        
        response = self.get_response(request)
        return response