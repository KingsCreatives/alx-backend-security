from ipware import get_client_ip
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django_ip_geolocation.utils import get_geolocation
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
            
            geo_data = cache.get(ip)

            if geo_data is None:
                geo_data = get_geolocation(ip)
                cache.set(ip, geo_data, timeout=86400)
            
            country = geo_data.get('country_name')
            city = geo_data.get('city')

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city,
            )

        response = self.get_response(request)
        return response