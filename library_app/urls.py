from django.contrib import admin
from django.urls import path
from . import views

app_name='library_app'


urlpatterns = [
    # Acutal Pages
    path('', views.index, name="index"),
    path('library/', views.library, name="library"),
    path('loaned_units/', views.loaned_units, name="loaned_units"),
    path('outstanding/', views.outstanding, name="outstanding"),
   
    # Book related
    path('add_book', views.add_book, name="add_book"),
    path('delete_book', views.delete_book, name="delete_book"),
    path('loan_book/', views.loan_book, name="loan_book"),
    path('unloan_book/', views.unloan_book, name="unloan_book"),

    # Magazine related
    path('add_magazine', views.add_magazine, name="add_magazine"),
    path('delete_magazine', views.delete_magazine, name="delete_magazine"),
    path('loan_magazine/', views.loan_magazine, name="loan_magazine"),
    path('unloan_magazine/', views.unloan_magazine, name="unloan_magazine"),
]
