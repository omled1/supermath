from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Creating models

class User(AbstractUser):
    pass

# Model for problem sheets
class Sheet(models.Model):
    user_id = models.PositiveIntegerField() # Which user created this sheet
    sheet_name = models.CharField(max_length=50, default="SuperMath Correspondence Contest") # Name for the sheet
    sheet_subname = models.CharField(max_length=50, default="Time Limit: 4 Minutes") # Subtitles for the sheet
    problem_data = models.JSONField() # All of the problem data of the sheet
    sheet_type = models.CharField(max_length=20) # Type of sheet (multiplication, division, arithmetic)
    created = models.DateTimeField(default=datetime.utcnow()) # Time sheet was created
    modified = models.DateTimeField(default=datetime.utcnow()) # Time sheet was modified