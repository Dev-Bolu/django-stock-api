from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import StoreItem, BarStock


@receiver(post_save, sender=StoreItem)
def sync_bar_stock_with_store_out(sender, instance, **kwargs):
    """
    When a StoreItem's store_out changes, automatically update or create
    today's BarStock record for that item with matching added_stock.
    """

    # Step 1: Safely update remaining stock (avoid recursion by using update())
    expected_remaining = instance.store_in - instance.store_out
    if instance.remaining_stock != expected_remaining:
        StoreItem.objects.filter(pk=instance.pk).update(remaining_stock=expected_remaining)

    # Step 2: Ensure a bar record exists for today
    bar_record, created = BarStock.objects.get_or_create(
        item=instance,
        record_date=date.today(),
        defaults={'open_stock': 0, 'added_stock': 0, 'sold': 0}
    )

    # Step 3: Sync added_stock with store_out (difference since yesterday)
    # We assume store_out reflects *total* moved to bar, not daily increment.
    bar_record.added_stock = instance.store_out
    bar_record.save(update_fields=['added_stock'])
