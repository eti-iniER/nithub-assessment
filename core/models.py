from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.managers import UserManager

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
        return self.email

    def __repr__(self):
        return f"<User: id={self.id} email={self.email}>"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    available_quantity = models.PositiveIntegerField()
    last_restocked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Product: id={self.id} name={self.name}>"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    def __repr__(self):
        return f"<Order: id={self.id} user={self.user}>"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name

    def __repr__(self):
        return f"<OrderItem: id={self.id} order_id={self.order.id} product={self.product.name}>"
