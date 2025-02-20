from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.managers import UserManager, OrderManager
from core.querysets import ProductQuerySet
from core.constants import DELETED_PRODUCT_ID

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __repr__(self):
        return f"<User: id={self.id} email={self.email}>"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    available_quantity = models.PositiveIntegerField(default=1)
    last_restocked = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Product: id={self.id} name={self.name}>"

    def save(self, *args, **kwargs):
        if self.pk:
            old_product = (
                Product.objects.filter(pk=self.pk).only("available_quantity").first()
            )
            if old_product and self.available_quantity > old_product.available_quantity:
                self.last_restocked = (
                    timezone.now()
                )  # Update last_restocked only if stock increased

        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return f"Order #{self.id}"

    def __repr__(self):
        return f"<Order: id={self.id} user={self.user}>"

    @property
    def description(self):
        items = list(self.items.all()[:2])
        item_strs = ", ".join(str(item) for item in items)

        if self.items.count() > 2:
            remaining = self.items.count() - 2
            item_strs += f" and {remaining} more item(s)"

        return item_strs

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)

        total_price = (
            self.items.aggregate(total_price=models.Sum("total_price_at_purchase"))[
                "total_price"
            ]
            or 0
        )
        self.total_price = total_price
        super().save(
            update_fields=["total_price"]
        )  # Save again with updated total_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_DEFAULT, default=DELETED_PRODUCT_ID
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price_at_purchase = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    def __repr__(self):
        return f"<OrderItem: id={self.id} order_id={self.order.id} product={self.product.name}>"

    def save(self, *args, **kwargs):
        # Prevent users from ordering the deleted product
        if self.product.id == DELETED_PRODUCT_ID:
            raise ValidationError("You cannot order a deleted product.")

        self.total_price_at_purchase = self.quantity * self.product.price
        super().save(*args, **kwargs)
