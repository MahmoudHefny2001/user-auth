from apps.users.models import User
from apps.users.managers import UserManager


class MerchantManager(UserManager):

    """
    This is a custom manager for the Merchant model.
    It is used to filter the Merchant from the User model.
    """

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MERCHANT)
    

    def create_merchant(self, email, full_name, phone_number, password, **extra_fields):
        """
        This method creates a new merchant.
        """
        return self.create_user(email, full_name, phone_number, password, role=User.Role.MERCHANT, **extra_fields)