from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .validators import valid_username, valid_phone_number, valid_password

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    This is the User model.
    It is used to create a User instance - for all project users '/as base model/' - .
    And it is used as a base model for all app users.
    Simulates an abstract class that have all common properties of all users.
    """
    
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Admin"
        # MANAGER = "MANAGER", "Manager"
        # SUPERVISOR = "SUPERVISOR", "Supervisor"
        # STAFF = "STAFF", "Staff",


    # base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices, null=True, blank=True, default=Role.CUSTOMER)
    
    
    full_name = models.CharField(max_length=100, blank=False, null=False,)

    email = models.EmailField(unique=True, db_index=True, null=True, blank=True)

    password = models.CharField(max_length=128, null=True, blank=True)

    phone_number = models.CharField(
        max_length=20, blank=True, 
        null=True, unique=True, db_index=True,
        validators=[valid_phone_number]
        ,
    )

    objects = UserManager()

    is_superuser = models.BooleanField(default=False, blank=True, null=True)

    is_staff = models.BooleanField(default=False, blank=True, null=True)

    
    USERNAME_FIELD = "email"
    
    EMAIL_FIELD = 'phone_number'

    REQUIRED_FIELDS = ["full_name",]



    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "users"
        