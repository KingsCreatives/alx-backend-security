from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies_hourly():
    """
    Flags IPs with excessive requests (>100/hr) or repeated access to sensitive paths.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # 1. Identify IPs with excessive requests (>100/hour)
    high_traffic_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
        .values('ip_address') \
        .annotate(request_count=Count('ip_address')) \
        .filter(request_count__gt=100) \
        .order_by('-request_count')

    for entry in high_traffic_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': f"Exceeded 100 requests in one hour (Count: {entry['request_count']})"}
        )
        print(f"Flagged high-traffic IP: {ip}")
        
    sensitive_paths = ['/admin/', '/login/'] 
    
    suspicious_path_traffic = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address') \
    .annotate(hit_count=Count('ip_address')) \
    .filter(hit_count__gt=10) 

    for entry in suspicious_path_traffic:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': f"Repeated access to sensitive paths ({entry['hit_count']} times)"}
        )
        print(f"Flagged sensitive access IP: {ip}")