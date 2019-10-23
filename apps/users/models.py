import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    uuid = models.CharField(max_length=36, default=str(uuid.uuid4()), blank=False, null=False)
    name = models.CharField(max_length=85, blank=False, null=False)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
