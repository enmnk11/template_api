from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Users
    path('api/auth/', include('apps.users.urls')),
    # Escribe tus endpoints aquí
]
