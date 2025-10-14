from django.db import models
from datetime import date

# Create your models here.
class StoreItem(models.Model):
    item = models.CharField(max_length=100, unique=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=0) # Cost price per item
    selling_price = models.DecimalField(max_digits=10, decimal_places=0) # Selling
    store_in = models.PositiveIntegerField(default=0) # Total received into store
    store_out = models.PositiveIntegerField(default=0) # Total moved out from store
    remaining_stock = models.PositiveIntegerField(default=0) # remaining stock in store

    def __str__(self):
        return self.item
    
    def update_remaining_stock(self):
        ''' Remaining stock calculation = store_in - store_out  '''
        self.remaining_stock = self.store_in - self.store_out
        self.save()
        
class BarStock(models.Model):
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='bar_stocks')
    record_date = models.DateField(default=date.today)
    open_stock = models.PositiveIntegerField(default=0) # opening stock in bar
    added_stock = models.PositiveIntegerField(default=0) # stock added to bar
    sold = models.PositiveIntegerField(default=0) # stock sold from bar
    closing_stock = models.PositiveIntegerField(default=0, editable=False) # closing stock in bar
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, editable=False) # total sales amount
    profit = models.DecimalField(max_digits=10, decimal_places=0, default=0, editable=False) # total profit amount
    
    def save(self, *args, **kwargs):
        ''' Closing stock calculation = opening stock + added stock - sold '''
        self.closing_stock = self.open_stock + self.added_stock - self.sold
        
        # Update total sales value and profit
        self.total_price = self.sold * self.item.selling_price  
        self.profit = self.sold * (self.item.selling_price - self.item.cost_price)
        #Update store when goods move out to bar
        if self.added_stock > 0:
            self.item.store_out += self.added_stock
            self.item.update_remaining_stock()
            self.item.save()  # Save changes to the related item
        super().save(*args, **kwargs)
        
    @property
    def total_stock_availale(self):
        ''' Total stock available = item in store and bar '''
        return (
            self.item.remaining_stock
            + self.item.store_in
            - self.item.store_out
            + self.open_stock
            + self.added_stock
            - self.sold
            
        )

    def __str__(self):
        return f"{self.item.item} - {self.record_date}"
    
    
    @property
    def is_low_stock(self):
        ''' Check if stock is low '''
        LOW_STOCK_THRESHOLD = 10  # Define your low stock threshold here
        return self.closing_stock < LOW_STOCK_THRESHOLD