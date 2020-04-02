from django.contrib import admin
from django.urls import path, include

app_name = 'login_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library_app.urls')),
    path('accounts/', include('login_app.urls')),
]
