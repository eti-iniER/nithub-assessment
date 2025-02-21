def test_order_total_price(db, product_factory, order_factory, order_item_factory):
    product1 = product_factory.create(price=3000)
    product2 = product_factory.create(price=5000)

    order = order_factory.create()
    order_item_factory.create(
        order=order, product=product1, quantity=2
    )  # 2 * 3000 = 6000
    order_item_factory.create(
        order=order, product=product2, quantity=1
    )  # 1 * 5000 = 5000

    # recreate the Order instance to get the updated total_price
    order.refresh_from_db()
    assert order.total_price == 11000
