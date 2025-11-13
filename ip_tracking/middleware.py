from ipware import get_client_ip
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = list(BlockedIP.objects.values_list('ip_address'))

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        if ip is not None:
            if ip in self.blocked_ips:
                return HttpResponseForbidden("Access Denied: Your IP address is blacklisted")
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
            )
        response = self.get_response(request)
        return response