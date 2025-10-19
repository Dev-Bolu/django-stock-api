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
    list_editable = ( 'sold',)
    list_filter = ('record_date', 'item__item')
    ordering = ('-record_date', 'item')


@admin.register(ItemValue)
class ItemValueAdmin(admin.ModelAdmin):
    list_display = ('item', 'date_recorded', 'sold', 'cost_price', 'selling_price', 'total_price', 'profit')
    readonly_fields = ('total_price', 'profit')
    list_filter = ('date_recorded', 'item__item')
    ordering = ('-date_recorded', 'item')
    

    def get_fields(self, request, obj=None):
        """Control which fields are visible on the form."""
        fields = super().get_fields(request, obj)
        if request.user.groups.filter(name='Staff').exists() and not request.user.is_superuser:
            # Staff see only 'sold'
            return ['sold']
        return fields  # Managers/superusers see all

    def get_readonly_fields(self, request, obj=None):
        """Protect other fields even if they somehow appear."""
        if request.user.groups.filter(name='Staff').exists() and not request.user.is_superuser:
            return []  # 'sold' is editable, others are hidden
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        """Ensure staff can only change 'sold' field."""
        if request.user.groups.filter(name='Staff').exists() and not request.user.is_superuser:
            if obj.pk:
                original = type(obj).objects.get(pk=obj.pk)
                # Restore other fields to their original values
                for field in self.model._meta.fields:
                    if field.name != 'sold':
                        setattr(obj, field.name, getattr(original, field.name))
        super().save_model(request, obj, form, change)
        
        
        
        