from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
from django.core.validators import validate_ipv46_address

class Command(BaseCommand):
    help = 'Blocks a specified IP address.'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        
        try:
            validate_ipv46_address(ip_address)
        except:
            raise CommandError(f'"{ip_address}" is not a valid IP address.')

        try:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: "{ip_address}"'))

        except Exception as e:
            
            raise CommandError(f'Could not block IP "{ip_address}": {e}')