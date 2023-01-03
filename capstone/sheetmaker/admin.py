from django.contrib import admin
# from sheetmaker.models import User
from django.contrib.auth.models import User

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, AuthorAdmin)
