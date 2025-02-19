from django.db.models.signals import post_migrate, post_save
from django.db.models import Sum
from django.dispatch import receiver
from core.models import Product, OrderItem
from core.constants import DELETED_PRODUCT_ID


@receiver(post_migrate)
def create_deleted_product(sender, **kwargs):
    """Ensures a 'Deleted Product' entry exists."""

    if not Product.objects.filter(id=DELETED_PRODUCT_ID).exists():
        Product.objects.create(
            id=DELETED_PRODUCT_ID,
            name="Deleted Product",
            price=0,
            description="This product was deleted",
        )


@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    total_price = (
        instance.order.items.aggregate(total_price=Sum("total_price_at_purchase"))[
            "total_price"
        ]
        or 0
    )
    instance.order.total_price = total_price
    instance.order.save(update_fields=["total_price"])


@receiver(post_save, sender=OrderItem)
def update_product_available_quantity(sender, instance, **kwargs):
    product_id = instance.product.id
    Product.objects.decrease_stock(product_id, instance.quantity)
