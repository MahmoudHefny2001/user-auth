from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .validators import valid_username, valid_phone_number, valid_password

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=50, unique=True, validators=[valid_username])
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True, validators=[valid_phone_number])

    objects = UserManager()

    password = models.CharField(max_length=200, validators=[valid_password])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        