from django.http import HttpResponseForbidden
from django.contrib.auth.views import redirect_to_login

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the admin site
        if request.path.startswith('/talhakhan/'):
            # Allow access to login page
            if request.path == '/talhakhan/login/' or request.path.startswith('/talhakhan/login'):
                return self.get_response(request)
                
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
                
            # Check if user is staff or superuser
            if not (request.user.is_staff or request.user.is_superuser):
                return HttpResponseForbidden("Access denied. Only staff and superusers can access the admin area.")
        
        # Continue processing the request
        return self.get_response(request)
