from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
from django.db import transaction
from .models import StoreItem, StoreItemHistory, BarStock, ItemValue
from django.conf import settings
from rest_framework.authtoken.models import Token


# -----------------------
# StoreItem → StoreItemHistory
# -----------------------
@receiver(post_save, sender=StoreItem)
def create_daily_storeitem_history(sender, instance, **kwargs):
    today = date.today()

    with transaction.atomic():
        history, created = StoreItemHistory.objects.get_or_create(
            item=instance,
            record_date=today,
            defaults={
                'store_in': instance.store_in or 0,
                'store_out': instance.store_out or 0,
                'remaining_stock': (instance.store_in or 0) - (instance.store_out or 0),
            }
        )

        # Always update values if they change
        history.store_in = instance.store_in or 0
        history.store_out = instance.store_out or 0
        history.remaining_stock = (instance.store_in or 0) - (instance.store_out or 0)
        history.save(update_fields=['store_in', 'store_out', 'remaining_stock'])


# -----------------------
# StoreItem -> BarStock
# -----------------------
@receiver(post_save, sender=StoreItem)
def sync_barstock_added_stock(sender, instance, **kwargs):
    today = date.today()
    yesterday = today - timedelta(days=1)

    with transaction.atomic():
        bar_stock, created = BarStock.objects.get_or_create(
            item=instance,
            record_date=today,
            defaults={'open_stock': 0, 'added_stock': 0, 'sold': 0}
        )

        # Carry forward yesterday's closing stock
        try:
            yesterday_stock = BarStock.objects.get(item=instance, record_date=yesterday)
            bar_stock.open_stock = yesterday_stock.closing_stock
        except BarStock.DoesNotExist:
            bar_stock.open_stock = 0

        # Sync added_stock with daily total
        if bar_stock.added_stock != instance.store_out:
            bar_stock.added_stock = instance.store_out or 0

        bar_stock.save(update_fields=['open_stock', 'added_stock'])


# -----------------------
# BarStock -> ItemValue
# -----------------------
@receiver(post_save, sender=BarStock)
def create_daily_item_value(sender, instance, **kwargs):
    today = instance.record_date
    store_item = instance.item

    with transaction.atomic():
        item_value, created = ItemValue.objects.get_or_create(
            item=store_item,
            date_recorded=today,
            defaults={
                'sold': instance.sold or 0,
                'cost_price': store_item.cost_price,
                'selling_price': store_item.selling_price,
            }
        )

        item_value.sold = instance.sold or 0
        item_value.cost_price = store_item.cost_price
        item_value.selling_price = store_item.selling_price
        item_value.total_price = (instance.sold or 0) * store_item.selling_price
        item_value.profit = (instance.sold or 0) * (store_item.selling_price - store_item.cost_price)
        item_value.save(update_fields=['sold', 'cost_price', 'selling_price', 'total_price', 'profit'])

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)