from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email=None, full_name=None, phone_number=None, password=None, **extra_fields):
        if email:
            
            email = self.normalize_email(email)
            user = self.model(
                email=email,
                full_name=full_name,
                phone_number=phone_number,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email=None, full_name=None, phone_number=None, password=None, **extra_fields):
        if not email or phone_number:
            raise ValueError('The Email or Phone must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # set the user role to admin
        extra_fields.setdefault('role', self.model.Role.ADMIN)

        return self.create_user(email, full_name, phone_number, password, **extra_fields)