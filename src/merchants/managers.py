from users.models import User
from users.managers import UserManager


class MerchantManager(UserManager):

    """
    This is a custom manager for the Merchant model.
    It is used to filter the Merchant from the User model.
    """

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MERCHANT)