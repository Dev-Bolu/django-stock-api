from django.core.management.base import BaseCommand
from datetime import date
from inventory.models import StoreItem, BarStock


class Command(BaseCommand):
    help = "Load structured test data for StoreItem and BarStock models"

    def handle(self, *args, **options):
        items_data = {
            "33": 725,
            "5 alive pulpy": 1166,
            "Action bitter pet": 294,
            "andre rose": 9200,
            "Bacardi Gold": 15000,
            "Bacardi White": 13000,
            "baron": 5000,
            "belaire rose": 70000,
            "best cream big": 5300,
            "best cream small": 1400,
            "best whiskey big": 3500,
            "best whiskey small": 1000,
            "big Heineken": 1350,
            "big stout": 1333,
            "black bullet": 1870,
            "Black goldberg": 658,
            "blue bullet": 1000,
            "budwier": 875,
            "campari": 15333,
            "Captain Jack": 2800,
            "chandor": 4000,
            "chi active": 1350,
            "chi exotic": 1250,
            "climax": 600,
            "coco samba": 350,
            "coke": 400,
            "Coke plastic": 358,
            "desperado bottle": 803,
            "desperado can": 812,
            "fanta": 400,
            "fayrouz can": 479,
            "Fearless": 358,
            "four cousin": 6500,
            "goldberg bottle": 725,
            "goldberg can": 600,
            "guiness stout can": 900,
            "Gulder": 866,
            "heineken can": 600,
            "Henessy small": 30000,
            "Hennessy VS": 29400,
            "Hennessy VSOP": 90000,
            "hollandia": 1600,
            "jack daniel's": 25000,
            "jager melter": 12500,
            "jameson black": 35000,
            "jameson green": 20000,
            "jekomo": 320,
            "Lacoco": 375,
            "M/Heineken": 760,
            "Maltina bottle": 541,
            "maltina can": 550,
            "Martel blue swift": 70000,
            "Martel vs": 45000,
            "matini rose": 12500,
            "medium stout": 900,
            "moet rose": 50000,
            "monster": 900,
            "Origin beer can": 750,
            "Origin bitters": 3166,
            "origin pet (NEW)": 938,
            "Peaks Yoghurt": 1520,
            "power horse": 1600,
            "Prediator": 417,
            "red bull": 1200,
            "red label": 19500,
            "remy martins": 70000,
            "rich lady": 3500,
            "robertson": 6500,
            "sierra tequla": 15000,
            "Smirnoff CAN": 600,
            "sprite": 400,
            "star radler": 600,
            "super komando": 258,
            "tiger": 725,
            "trophy bottle": 708,
            "trophy can": 600,
            "viju yoghurt": 500,
            "water": 125,
        }

        self.stdout.write(self.style.MIGRATE_HEADING("Generating model-based test data..."))

        created_items = 0
        created_bars = 0

        for item_name, cost in items_data.items():
            # Create store item
            store_item, created = StoreItem.objects.get_or_create(
                item=item_name.strip(),
                defaults={
                    "store_in": 100,
                    "store_out": 0,
                    "remaining_stock": 100,
                },
            )
            if created:
                created_items += 1

            # Create related BarStock
            selling_price = cost * 2
            bar_stock, bar_created = BarStock.objects.get_or_create(
                item=store_item,
                record_date=date.today(),
                defaults={
                    "open_stock": 20,
                    "added_stock": 10,
                    "sold": 5,
                    "closing_stock": 0,  # model will recalculate on save()
                    "cost_price": cost,
                    "selling_price": selling_price,
                },
            )
            if bar_created:
                created_bars += 1
                bar_stock.save()  # triggers model logic to compute profit/closing

        self.stdout.write(self.style.SUCCESS(f"✅ StoreItem created: {created_items}"))
        self.stdout.write(self.style.SUCCESS(f"✅ BarStock created: {created_bars}"))
        self.stdout.write(self.style.SUCCESS("Test data generation complete!"))
