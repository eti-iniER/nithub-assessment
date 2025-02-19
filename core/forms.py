from django import forms
from core.models import Product, OrderItem
from core.constants import DELETED_PRODUCT_ID
from core.utils import convert_kobo_to_naira, convert_naira_to_kobo


class ProductAdminForm(forms.ModelForm):
    price_in_naira = forms.FloatField(label="Price (₦)")

    class Meta:
        model = Product
        fields = ["name", "price_in_naira", "description", "available_quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["price_in_naira"].initial = convert_kobo_to_naira(
                self.instance.price
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.price = convert_naira_to_kobo(self.cleaned_data["price_in_naira"])
        if commit:
            instance.save()
        return instance


class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].queryset = Product.objects.filter(
            available_quantity__gt=0
        ).exclude(id=DELETED_PRODUCT_ID)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        product = self.cleaned_data["product"]

        if product and quantity > product.available_quantity:
            raise forms.ValidationError(
                f"Only {product.available_quantity} items available."
            )
        return quantity
