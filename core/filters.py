from django.contrib import admin
from core.constants import LOW_STOCK_THRESHOLD


class StockStatusFilter(admin.SimpleListFilter):
    title = "stock status"
    parameter_name = "stock_status"

    def lookups(self, request, model_admin):
        return [
            ("available", "Available"),
            ("low_stock", "Low stock"),
            ("out_of_stock", "Out of stock"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "out_of_stock":
            return queryset.filter(available_quantity=0)
        elif self.value() == "available":
            return queryset.available()
        elif self.value() == "low_stock":
            return queryset.filter(available_quantity__lte=LOW_STOCK_THRESHOLD)
        return queryset
