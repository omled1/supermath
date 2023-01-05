from django.contrib import admin
from sheetmaker.models import User, Sheet

# Registering models
admin.site.register(User)
admin.site.register(Sheet)