from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True) # Forzamos que el email sea único

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
