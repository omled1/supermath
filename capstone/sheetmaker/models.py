from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    pass

class Sheet(models.Model):
    user_id = models.PositiveIntegerField()
    sheet_name = models.CharField(max_length=50, default="Supermath Correspondence Contest")
    problem_data = models.JSONField()
    sheet_type = models.CharField(max_length=20)
    created = models.DateTimeField(default=datetime.now())
    modified = models.DateTimeField(default=datetime.now())