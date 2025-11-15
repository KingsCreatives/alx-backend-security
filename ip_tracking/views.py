from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
import logging

logger = logging.getLogger(__name__)

@ratelimit(key='ip', rate='10/m', method=ratelimit.ALL, block=True)
@ratelimit(key='ip', rate='5/m', method=ratelimit.ALL, block=True)
def sensitive_data_view(request):
    """
    A view that demonstrates rate limiting.
    The decorators apply a limit based on the user being authenticated or anonymous.
    """
    
    if request.user.is_authenticated:
        limit_used = '10/m (Authenticated)'
    else:
        limit_used = '5/m (Anonymous)'
        
    logger.info(f"Sensitive view accessed by {request.META.get('REMOTE_ADDR')}. Limit: {limit_used}")
    
    return HttpResponse(f"Access granted. Request Count: {request.ratelimit.gets}/{request.ratelimit.limit}")