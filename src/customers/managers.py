from users.models import User
from users.managers import UserManager


class CustomerManager(UserManager):

    """
    This is a custom manager for the Customer model.
    It is used to filter the Customer from the User model.
    """

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)