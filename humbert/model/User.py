from django.db import models
from django.contrib.auth.models import User

class Profile(User):
    fb_id = models.IntegerField(default=0)

    class Meta:
        app_label = "humbert"
