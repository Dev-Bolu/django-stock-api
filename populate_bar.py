from inventory.models import StoreItem
from decimal import Decimal

def run():
    StoreItem.objects.all().delete()
    print("🗑️ Old items deleted.\n")

    items_data = [
        ("33 Export", 400, 600, 50), ("5 Alive Pulpy", 700, 1000, 20), ("Action Bitter Pet", 200, 300, 100),
        ("Andre Rose", 3500, 5000, 10), ("Bacardi Gold", 4500, 6000, 5), ("Bacardi White", 4500, 6000, 5),
        ("Baron", 3000, 4000, 8), ("Belaire Rose", 15000, 20000, 3), ("Best Whiskey Small", 500, 700, 40),
        ("Best Cream Medium", 800, 1000, 35), ("Best Whiskey Big", 1200, 1500, 25), ("Best Whiskey Medium", 900, 1100, 30),
        ("Best Cream Big", 1500, 2000, 15), ("Big Stout", 700, 1000, 50), ("Black Bullet", 700, 1000, 50),
        ("Black Goldberg", 600, 800, 50), ("Black Trophy", 600, 800, 50), ("Blue Bullet", 700, 1000, 50),
        ("Budweiser", 800, 1000, 50), ("Campari", 2500, 3500, 20), ("Captain Jack", 900, 1200, 25),
        ("Chandor", 1500, 2000, 15), ("Chi Active", 700, 1000, 20), ("Chi Exotic", 700, 1000, 20),
        ("Climax", 500, 700, 60), ("Coco Samba", 600, 800, 50), ("Coke", 400, 600, 100),
        ("Desperado Bottle", 1200, 1500, 20), ("Eliot", 700, 900, 40), ("Fanta", 400, 600, 80),
        ("Fayrouz Can", 500, 700, 50), ("Fearless", 500, 700, 50), ("Four Cousins", 3500, 4500, 10),
        ("Goldberg Bottle", 600, 800, 80), ("Guinness Stout Can", 800, 1000, 60), ("Gulder", 700, 900, 60),
        ("Hennessy Small", 7500, 10000, 5), ("Hennessy VS", 15000, 20000, 3), ("Hennessy VSOP", 25000, 30000, 2),
        ("Hollandia", 600, 800, 50), ("Jack Daniel's", 18000, 22000, 2), ("Jager Melter", 6000, 7500, 4),
        ("Jameson Black", 17000, 20000, 3), ("Jameson Green", 15000, 18000, 3), ("Jekomo", 700, 900, 40),
        ("Lacoco", 700, 900, 40), ("M/Heineken", 900, 1200, 60), ("Maltina Can", 500, 700, 50),
        ("Martel Blue Swift", 18000, 22000, 2), ("Martel VS", 15000, 20000, 3), ("Martini Rose", 7000, 9000, 4),
        ("M/ Stout", 900, 1200, 50), ("Moet Rose", 25000, 30000, 2), ("Monster", 800, 1000, 30),
        ("Origin Beer Bottle", 700, 900, 60), ("Origin Beer Can", 800, 1000, 40), ("Origin Bitters Bottle", 700, 900, 50),
        ("Origin Pet (New)", 600, 800, 70), ("Peaks Yoghurt", 500, 700, 50)
    ]

    for name, cost, sell, stock in items_data:
        StoreItem.objects.create(
            item=name,
            cost_price=Decimal(cost),
            selling_price=Decimal(sell),
            store_in=stock,
            remaining_stock=stock
        )
        print(f"✅ {name} added.")

    print("\n🎉 All items added successfully.")
