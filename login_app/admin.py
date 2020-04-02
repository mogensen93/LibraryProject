from django.contrib import admin
from .models import RequestPasswordReset, User_Access_Level

admin.site.register(RequestPasswordReset)
admin.site.register(User_Access_Level)