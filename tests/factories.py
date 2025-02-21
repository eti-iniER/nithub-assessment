import factory
from faker import Faker
from core.models import User, Product, Order, OrderItem
from core.utils import convert_naira_to_kobo
from django.contrib.auth.hashers import make_password

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = make_password(fake.password())
    is_active = True
    is_staff = False


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = fake.sentence(5, True)
    description = fake.text(16)
    price = convert_naira_to_kobo(fake.random_int(min=100, max=10000))
    available_quantity = fake.random_int(min=100, max=2000)
    last_restocked = fake.past_datetime()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = factory.LazyAttribute(
        lambda obj: fake.random_int(min=1, max=obj.product.available_quantity)
    )
    total_price_at_purchase = factory.LazyAttribute(
        lambda obj: obj.product.price * obj.quantity
    )
