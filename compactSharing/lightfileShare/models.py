from django.db import models
from django.conf import settings

from datetime import datetime, timedelta, timezone

import os

# Create your models here.


def expire_time_maker(lifetime_in_hour=settings.MY_DEFAULT_FILE_LIFETIME_IN_HOUR): # default config : last for 3 days
    targettime = datetime.now(tz=timezone.utc) + timedelta(hours=lifetime_in_hour)
    return targettime


class SecretFileManager(models.Manager):
    
    def remove_not_exist(self):
        for obj in self.all():
            if not os.path.exists( settings.MEDIA_ROOT / obj.content.name ):
                obj.delete()
    
    def remove_expired(self):
        for obj in self.all():
            if datetime.now(timezone.utc) > obj.expire_at:
                obj.delete()
        



class SecretFile(models.Model):

    class PrivateLevel:
        Init = -1
        Public = 0
        MiddleManager = 1
        Superuser = 2

    privatelevel = models.IntegerField(blank=True, null=False, default=PrivateLevel.Init)
    password = models.CharField(blank=True, null=True, max_length=1024) # string salted+hashed by 'my_hash()'
    title = models.CharField(blank=True, null=False, default='', max_length=100)
    content = models.FileField(blank=False, null=False, upload_to=settings.LIGHTFILE_SAVE_DIR)
    posted_by = models.CharField(blank=True, null=False, default='AnonymousUser', max_length=100)
    expire_at = models.DateTimeField(blank=True, null=False, default=expire_time_maker)


    objects = SecretFileManager()
