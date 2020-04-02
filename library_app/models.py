from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    publish_date = models.DateTimeField()
    added_to_library = models.DateTimeField(auto_now_add=True)

    loaner = models.CharField(max_length=100, default="none")
    loaned_out = models.BooleanField(default=False)
    loaned_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'Title: {self.title} --- Timestamp: {self.loaned_date} --- Loaned: {self.loaned_out} --- Loaner: {self.loaner} -- Return: {self.return_date}'

class Magazine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    publish_date = models.DateTimeField()
    added_to_library = models.DateTimeField(auto_now_add=True)

    loaner = models.CharField(max_length=100, default="none")
    loaned_out = models.BooleanField(default=False)
    loaned_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'Title: {self.title} --- Timestamp: {self.loaned_date} --- Loaned: {self.loaned_out} --- Loaner: {self.loaner} -- Return: {self.return_date}'

class User_Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book_count = models.IntegerField(default=0)
    magazine_count = models.IntegerField(default=0)

    def __str__(self):
        return f'User: {self.user} --- Book Count: {self.book_count} --- Mag Count: {self.magazine_count}'

