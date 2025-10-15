from django.db import models
from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError


class StoreItem(models.Model):
    """
    Master catalog of items in the store.
    """
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
        self.remaining_stock = (self.store_in or 0) - (self.store_out or 0)
        self.save(update_fields=["remaining_stock"])


class StoreItemHistory(models.Model):
    """
    Daily snapshot of store movements for each item.
    """
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='history')
    record_date = models.DateField(default=date.today)
    store_in = models.PositiveIntegerField(default=0)
    store_out = models.PositiveIntegerField(default=0)
    remaining_stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('item', 'record_date')

    def __str__(self):
        return f"{self.item.item} - {self.record_date}"


class BarStock(models.Model):
    """
    Daily bar movement for each item.
    """
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='bar_stocks')
    record_date = models.DateField(default=date.today)
    open_stock = models.PositiveIntegerField(default=0)
    added_stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    closing_stock = models.PositiveIntegerField(default=0, editable=False)

    def clean(self):
        if self.sold > (self.open_stock + self.added_stock):
            raise ValidationError("Sold quantity cannot exceed available stock.")

    def save(self, *args, **kwargs):
        self.closing_stock = (self.open_stock or 0) + (self.added_stock or 0) - (self.sold or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.item} - {self.record_date}"


class ItemValue(models.Model):
    """
    Daily financial tracking per item.
    Stores sold quantity, cost price, selling price, total price, and profit.
    """
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='item_values')
    date_recorded = models.DateField(default=date.today)
    sold = models.PositiveIntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    class Meta:
        unique_together = ('item', 'date_recorded')

    def save(self, *args, **kwargs):
        self.total_price = (self.sold or 0) * (self.selling_price or Decimal('0'))
        self.profit = (self.sold or 0) * ((self.selling_price or Decimal('0')) - (self.cost_price or Decimal('0')))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.item} - {self.date_recorded}"
