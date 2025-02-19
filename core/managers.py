from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager
from core.querysets import UserQuerySet, OrderQuerySet


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    """
    Custom user model manager where the user's email address is the unique identifier
    """

    def create_user(self, email, password, **fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("User email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **fields):
        """
        Create and save a superuser with the given email and password.
        """
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        fields.setdefault("is_active", True)

        if fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **fields)


class OrderManager(Manager.from_queryset(OrderQuerySet)):
    def create_order(self, user, items):
        from core.models import OrderItem

        order = self.create(user=user)

        order_items = [
            OrderItem(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                total_price_at_purchase=item["quantity"] * item["product"].price,
            )
            for item in items
        ]
        OrderItem.objects.bulk_create(order_items)

        return order
