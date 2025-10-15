from django.contrib import admin
from datetime import timedelta
from .models import StoreItem, StoreItemHistory, BarStock, ItemValue

@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'cost_price', 'selling_price', 'store_in', 'store_out', 'remaining_stock')
    readonly_fields = ('remaining_stock',)
    list_editable = ('cost_price', 'selling_price', 'store_in', 'store_out',)
    search_fields = ('item',)
    ordering = ('item',)


@admin.register(StoreItemHistory)
class StoreItemHistoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'record_date', 'store_in', 'store_out', 'remaining_stock')
    list_filter = ('record_date', 'item__item')
    ordering = ('-record_date', 'item')


@admin.register(BarStock)
class BarStockAdmin(admin.ModelAdmin):
    list_display = ('item', 'record_date', 'open_stock', 'added_stock', 'sold', 'closing_stock')
    list_editable = ('added_stock', 'sold',)
    list_filter = ('record_date', 'item__item')
    ordering = ('-record_date', 'item')


@admin.register(ItemValue)
class ItemValueAdmin(admin.ModelAdmin):
    list_display = ('item', 'date_recorded', 'sold', 'cost_price', 'selling_price', 'total_price', 'profit')
    readonly_fields = ('total_price', 'profit')
    list_filter = ('date_recorded', 'item__item')
    ordering = ('-date_recorded', 'item')
