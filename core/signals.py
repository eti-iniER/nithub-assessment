from django.db.models.signals import post_migrate
from django.dispatch import receiver
from core.models import Product


@receiver(post_migrate)
def create_deleted_product(sender, **kwargs):
    """Ensures a 'Deleted Product' entry exists."""

    if not Product.objects.filter(name="Deleted Product").exists():
        Product.objects.create(
            id=1,
            name="Deleted Product",
            price=0,
            description="This product was deleted",
        )
