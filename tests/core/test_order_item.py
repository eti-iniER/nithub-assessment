import pytest
from core.exceptions import InsufficientStockError


def test_cannot_order_more_than_stock(db, product_factory, order_item_factory):
    product = product_factory.create(available_quantity=5)

    with pytest.raises(InsufficientStockError):
        order_item_factory.create(product=product, quantity=10)
