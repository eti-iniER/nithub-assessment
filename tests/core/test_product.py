def test_order_decreases_stock(db, product_factory, order_item_factory):
    product = product_factory.create(available_quantity=10)
    order_item_factory.create(product=product, quantity=3)

    product.refresh_from_db()
    assert product.available_quantity == 7
