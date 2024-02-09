from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, 
                    # username, 
                    phone_number, full_name, password=None
        ):
        if not email:
            raise ValueError("Users must have an email address")
        # if not username:
        #     raise ValueError("Users must have a username")
        if not full_name:
            raise ValueError("Users must have a full name")

        user = self.model(
            email=self.normalize_email(email),
            # username=username,
            full_name=full_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, 
            # username, 
            phone_number, full_name, password=None
        ):
        user = self.create_user(
            email=self.normalize_email(email),
            # username=username,
            full_name=full_name,
            password=password,
            phone_number=phone_number,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user