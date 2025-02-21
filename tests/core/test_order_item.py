import pytest
from core.exceptions import InsufficientStockError


def test_cannot_order_more_than_stock(db, product_factory, order_item_factory):
    product = product_factory.create(available_quantity=5)

    with pytest.raises(InsufficientStockError):
        order_item_factory.create(product=product, quantity=10)


def test_order_item_price_does_not_change(db, product_factory, order_item_factory):
    product = product_factory.create(price=5000)
    order_item = order_item_factory.create(product=product, quantity=2)

    # Change product price
    product.price = 8000
    product.save()

    order_item.refresh_from_db()
    assert order_item.total_price_at_purchase == 10000  # 2 * 5000, NOT 2 * 8000
