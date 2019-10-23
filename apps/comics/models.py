import uuid
from django.db import models


# Create your models here.
class Comic(models.Model):
    uuid = models.CharField(max_length=36, default=str(uuid.uuid4()), blank=False, null=False, editable=False,
                            unique=True)
    comic = models.CharField(max_length=64, blank=False, null=False)
    author = models.CharField(max_length=64, blank=False, null=False)
    url = models.TextField(blank=False, null=False)
    description = models.CharField(max_length=512, blank=False, null=False)
    rewards = models.SmallIntegerField(blank=False, null=False)
    created_by = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    state = models.SmallIntegerField(default=1, blank=False, null=False)


class ComicsUrl(models.Model):
    uuid = models.CharField(max_length=36, blank=False, null=False,
                            unique=True)
    comic = models.ForeignKey(Comic, related_name="comics_url", blank=False, null=False, on_delete=models.CASCADE)
    url = models.TextField(blank=False, null=False)
    index = models.SmallIntegerField(blank=False, null=False)
    created_by = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    state = models.SmallIntegerField(default=1, blank=False, null=False)
