from django.db import models
from django.conf import settings

from datetime import datetime, timedelta, timezone

# Create your models here.


def expire_time_maker(lifetime_in_hour=settings.MY_DEFAULT_FILE_LIFETIME_IN_HOUR): # default config : last for 3 days
    targettime = datetime.now(tz=timezone.utc) + timedelta(hours=lifetime_in_hour)
    return targettime


class SecretClipboardManager(models.Manager):
    
    def remove_expired(self):
        for obj in self.all():
            if datetime.now(timezone.utc) > obj.expire_at:
                obj.delete()
        

class SecretClipboard(models.Model):
    
    password = models.CharField(blank=True, null=True, max_length=1024) # string salted+hashed by 'my_hash()'
    title = models.CharField(blank=True, null=False, default='', max_length=100)
    content = models.TextField(blank=False, null=False)
    posted_by = models.CharField(blank=True, null=False, default='anonymousUser', max_length=100)
    expire_at = models.DateTimeField(blank=True, null=False, default=expire_time_maker)
    
    
    objects = SecretClipboardManager()

