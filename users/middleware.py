from django.http import HttpResponseForbidden
from django.conf import settings

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Get allowed IPs from settings or use a default list
        self.allowed_ips = getattr(settings, 'ADMIN_ALLOWED_IPS', [])

    def __call__(self, request):
        # Check if the request is for the admin site
        if request.path.startswith('/admin/'):
            # Get client IP - handle proxy forwarding if needed
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                # Get the first IP in case of multiple proxies
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Check if IP is in allowed list
            if self.allowed_ips and ip not in self.allowed_ips:
                return HttpResponseForbidden("Access denied. Your IP is not authorized to access the admin area.")
        
        # Continue processing the request for allowed IPs or non-admin URLs
        return self.get_response(request)
