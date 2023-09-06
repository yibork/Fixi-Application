from django.contrib.auth.mixins import UserPassesTestMixin

class IsUserCreatedOrderOrAdmin(UserPassesTestMixin):
    """
    This mixin is used to check if the user is the one who created the order
    or if the user is an admin
    """
    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user or self.request.user.is_superuser:
            return True
        return False