from django.db import models
from secrets import token_urlsafe 
from django.contrib.auth.models import User

# Create your models here.

class RequestPasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=43, default=token_urlsafe)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'USER: {self.user} l CREATED TIMESTAMP: {self.created_timestamp} l TOKEN: {self.token} l UPDATED TIMESTAMP {self.updated_timestamp}'

class User_Access_Level(models.Model):
    type_of_user = (
        ('C', 'Customer'),
        ('S', 'Staff'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=1, choices=type_of_user)
    def __str__(self):
        return f'USER: {self.user} l Access_level: {self.access_level}'