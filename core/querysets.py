from django.db import models
from core.exceptions import InsufficientStockError, InvalidProductError
from core.constants import DELETED_PRODUCT_ID


class ProductQuerySet(models.QuerySet):
    def all_except_deleted(self):
        return self.exclude(id=DELETED_PRODUCT_ID)

    def available(self, required_quantity=1):
        return self.filter(available_quantity__gte=required_quantity)

    def restock(self, additional_quantity=1):
        return self.update(
            available_quantity=models.F("available_quantity") + additional_quantity
        )

    def restock_product(self, product_id, additional_quantity=1):
        return self.filter(id=product_id).update(
            available_quantity=models.F("available_quantity") + additional_quantity
        )

    def decrease_stock(self, product_id, quantity):
        """Atomically decrease stock while ensuring availability."""
        if not self.filter(id=product_id).exists():
            raise InvalidProductError(f"Product ID {product_id} does not exist.")
        elif product_id == DELETED_PRODUCT_ID:
            raise InvalidProductError(f"Product ID {product_id} is invalid.")

        updated_rows = self.filter(
            id=product_id, available_quantity__gte=quantity
        ).update(available_quantity=models.F("available_quantity") - quantity)

        if updated_rows == 0:
            raise InsufficientStockError(
                f"Not enough stock for Product ID {product_id}."
            )


class UserQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def staff(self):
        return self.filter(is_staff=True)

    def customers(self):
        return self.filter(is_staff=False)


class OrderQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(user=user)

    def total_price(self) -> int:
        return self.aggregate(total_price=models.Sum("total_price"))["total_price"] or 0

    def filter_by_date(self, date):
        return self.filter(created_at__date=date)
