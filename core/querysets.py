from django.db import models


class ProductQuerySet(models.QuerySet):

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
