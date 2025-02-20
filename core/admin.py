from django.contrib import admin
from core.models import User, Product, Order, OrderItem
from core.forms import ProductAdminForm, OrderItemInlineForm
from core.constants import DELETED_PRODUCT_ID
from core.utils import convert_kobo_to_naira
from django.contrib import admin
from django.db.models import Sum

# Register your models here.

admin.site.register(User)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "formatted_price",
        "description",
        "formatted_available_quantity",
    ]
    form = ProductAdminForm

    def formatted_price(self, obj):
        """Convert price from kobo to naira and format properly."""
        return f"₦{convert_kobo_to_naira(obj.price):,.2f}"

    def formatted_available_quantity(self, obj):
        return f"{obj.available_quantity:,}"

    formatted_price.short_description = "Price (₦)"
    formatted_available_quantity.short_description = "Available Quantity"

    def get_queryset(self, request):
        """Exclude the DeletedProduct from the admin product list."""
        queryset = super().get_queryset(request)
        return queryset.exclude(id=DELETED_PRODUCT_ID)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInlineForm
    extra = 0

    readonly_fields = ("product_price_at_purchase",)

    def product_price_at_purchase(self, obj):
        if obj.total_price_at_purchase and obj.quantity:
            price = convert_kobo_to_naira(obj.total_price_at_purchase // obj.quantity)
            return f"₦{price:,.2f}"
        return "N/A"

    product_price_at_purchase.short_description = "Price at Purchase (₦)"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "info",
        "description",
        "user",
        "formatted_price",
        "created_at",
    ]
    list_display_links = ["info"]
    inlines = [OrderItemInline]

    def info(self, obj):
        return str(obj)

    def formatted_price(self, obj):
        """Convert price from kobo to naira and format properly."""
        return f"₦{convert_kobo_to_naira(obj.total_price):,.2f}"

    formatted_price.short_description = "Total price"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        order = form.instance
        if order.total_price == 0:  # Only compute once
            total_price = (
                order.items.aggregate(total_price=Sum("total_price_at_purchase"))[
                    "total_price"
                ]
                or 0
            )
            order.total_price = total_price
            order.save(update_fields=["total_price"])
