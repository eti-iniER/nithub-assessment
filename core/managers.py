from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager, Sum
from core.querysets import UserQuerySet, OrderQuerySet
from core.exceptions import InsufficientStockError, InvalidProductError


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
        from core.models import OrderItem, Product

        # total_price = 0 is temporary. We will compute the total price shortly
        order = self.create(user=user, total_price=0)

        order_items = []

        for item in items:
            product = item["product"]
            quantity = item["quantity"]

            try:
                Product.objects.decrease_stock(product.id, quantity)
            except (InsufficientStockError, InvalidProductError) as e:
                order.delete()
                raise e

            order_item_total_price_at_purchase = quantity * product.price

            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    total_price_at_purchase=order_item_total_price_at_purchase,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        return order
