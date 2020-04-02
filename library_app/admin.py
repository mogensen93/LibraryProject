from django.contrib import admin
from .models import Book, User_Loan, Magazine

# Register your models here.
admin.site.register(Book)
admin.site.register(User_Loan)
admin.site.register(Magazine)