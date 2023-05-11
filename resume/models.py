import os
from datetime import datetime
import glob
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from resume_template.models import ResumeTemplate


def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "resume_image_" + \
        str(instance.id) + "_" + str(int(datetime.now().timestamp()))
    upload_to_path = "resume_images/{new_filename}.{ext}".format(new_filename=new_filename, ext=ext)
    old_thumnails = glob.iglob(os.path.join(str(settings.MEDIA_ROOT) + "/resume_images",
                                            "resume_image_" + str(instance.id) + '*'))
    for file in old_thumnails:
        if os.path.isfile(file):
            os.remove(file)
    return upload_to_path


def thumbnail_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "thumbnail_" + \
        str(instance.id) + "_" + str(int(datetime.now().timestamp()))
    upload_to_path = "resume_thumbnails/{new_filename}.{ext}".format(new_filename=new_filename, ext=ext)
    old_thumnails = glob.iglob(os.path.join(str(settings.MEDIA_ROOT) + "/resume_thumbnails",
                                            "thumbnail_" + str(instance.id) + '*'))
    for file in old_thumnails:
        if os.path.isfile(file):
            os.remove(file)
    return upload_to_path


# DYNAMIC UPLOAD_TO - handle later
# def path_and_rename(path):
#     def wrapper(instance, filename):
#         ext = filename.split('.')[-1]
#         new_filename = "{path}_".format(path=path) + str(instance.id)
#         upload_to_path = "{path}s/{new_filename}.{ext}".format(path=path, new_filename=new_filename, ext=ext)
#         full_path = str(settings.MEDIA_ROOT) + '/' + upload_to_path
#         if os.path.isfile(full_path):
#             os.remove(full_path)
#         return upload_to_path
#     return wrapper


class Resume(models.Model):
    title = models.TextField(default="Untitled")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_to,
        default="default_images/resume_thumbnails/new_resume_thumbnail.png",
        blank=True, null=True
    )
    completeness = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    layout = models.JSONField(null=True, blank=True)

    def __str__(self):
        username = self.user.username if self.user else "anonymous"
        return f'{self.title} - {username}'
