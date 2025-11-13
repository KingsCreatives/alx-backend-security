from django.db import models

# Create your models here.
class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField(
        verbose_name="IP Address",
        null=True,
        blank=True
    )
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} accessed {self.path} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(
        verbose_name="Blocked IP Address",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.ip_address
    class Meta:
        verbose_name_plural = "Blocked IPs"