from django.db import models
from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError


class StoreItem(models.Model):
    item = models.CharField(max_length=100, unique=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    store_in = models.PositiveIntegerField(default=0)
    store_out = models.PositiveIntegerField(default=0)
    remaining_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item

    def update_remaining_stock(self):
        """Remaining stock = store_in - store_out"""
        self.remaining_stock = self.store_in - self.store_out
        self.save(update_fields=["remaining_stock"])


class BarStock(models.Model):
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='bar_stocks')
    record_date = models.DateField(default=date.today)
    open_stock = models.PositiveIntegerField(default=0)
    added_stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    closing_stock = models.PositiveIntegerField(default=0, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    def clean(self):
        """Prevent invalid stock entries"""
        if self.sold > (self.open_stock + self.added_stock):
            raise ValidationError("Sold quantity cannot exceed available stock.")

    def save(self, *args, **kwargs):
        """Auto-calculate closing stock, sales, and profit"""
        self.closing_stock = self.open_stock + self.added_stock - self.sold
        self.total_price = Decimal(self.sold) * self.item.selling_price
        self.profit = Decimal(self.sold) * (self.item.selling_price - self.item.cost_price)
        super().save(*args, **kwargs)

    @property
    def total_stock_available(self):
        """Total stock available = remaining in store + bar closing stock"""
        return self.item.remaining_stock + self.closing_stock

    @property
    def is_low_stock(self):
        LOW_STOCK_THRESHOLD = 10
        return self.closing_stock < LOW_STOCK_THRESHOLD

    def __str__(self):
        return f"{self.item.item} - {self.record_date}"
