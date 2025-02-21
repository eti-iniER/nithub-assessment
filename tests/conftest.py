from pytest_factoryboy import register
from tests.factories import UserFactory, ProductFactory, OrderFactory, OrderItemFactory

register(UserFactory)
register(ProductFactory)
register(OrderFactory)
register(OrderItemFactory)
