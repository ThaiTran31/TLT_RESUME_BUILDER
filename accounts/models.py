import os
from datetime import datetime
import glob
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "avatar_" + \
        str(instance.id) + "_" + str(int(datetime.now().timestamp()))
    upload_to_path = "user_avatars/{new_filename}.{ext}".format(new_filename=new_filename, ext=ext)
    old_thumnails = glob.iglob(os.path.join(str(settings.MEDIA_ROOT) + "/user_avatars",
                                            "avatar_" + str(instance.id) + '*'))
    for file in old_thumnails:
        if os.path.isfile(file):
            os.remove(file)
    return upload_to_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=511, blank=True, null=True)
    city = models.CharField(max_length=127, blank=True, null=True)
    country = models.CharField(max_length=127, blank=True, null=True)
