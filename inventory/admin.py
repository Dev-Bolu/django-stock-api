from django.contrib import admin
from datetime import timedelta
from .models import StoreItem, BarStock


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'cost_price', 'selling_price', 'store_in', 'store_out', 'remaining_stock')
    readonly_fields = ('remaining_stock',)
    list_editable = ('cost_price', 'selling_price', 'store_in', 'store_out',)
    search_fields = ('item',)
    list_filter = ('item',)
    ordering = ('item',)


@admin.action(description="Carry forward today's closing stock as tomorrow's opening stock")
def carry_forward_opening_stock(modeladmin, request, queryset):
    """
    For each selected BarStock entry, create a new BarStock record for the next day
    with the closing_stock as open_stock (skip if next day record exists).
    """
    new_bar_stocks = []
    for bar_stock in queryset:
        next_day = bar_stock.record_date + timedelta(days=1)
        if not BarStock.objects.filter(item=bar_stock.item, record_date=next_day).exists():
            new_bar_stocks.append(
                BarStock(
                    item=bar_stock.item,
                    record_date=next_day,
                    open_stock=bar_stock.closing_stock,
                    added_stock=0,
                    sold=0
                )
            )
    if new_bar_stocks:
        BarStock.objects.bulk_create(new_bar_stocks)
        modeladmin.message_user(request, f"{len(new_bar_stocks)} next-day bar stock records created.")
    else:
        modeladmin.message_user(request, "No new records created — all next-day entries already exist.")


@admin.register(BarStock)
class BarStockAdmin(admin.ModelAdmin):
    list_display = ('item', 'record_date', 'open_stock', 'added_stock', 'sold',
                    'closing_stock', 'total_price', 'profit')
    search_fields = ('item__item',)
    list_filter = ('record_date', 'item__item')
    ordering = ('-record_date', 'item')
    actions = [carry_forward_opening_stock]

class LowStockFilter(admin.SimpleListFilter):
    title = 'Low Stock'
    parameter_name = 'low_stock'

    def lookups(self, request, model_admin):
        return (('yes', 'Low stock (<10)'),)

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(closing_stock__lt=10)
        return queryset

list_filter = ('record_date', 'item__item', LowStockFilter)
