import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT = Path("data/raw")
OUT.mkdir(parents=True, exist_ok=True)

products = [
    ("P1001", "Running Shoes", "Footwear", 79.99),
    ("P1002", "Performance T-Shirt", "Apparel", 29.99),
    ("P1003", "Training Shorts", "Apparel", 34.99),
    ("P1004", "Sports Jacket", "Outerwear", 119.99),
    ("P1005", "Backpack", "Accessories", 64.99),
]

warehouses = [
    ("W01", "Chicago DC", "Chicago", "IL"),
    ("W02", "Dallas DC", "Dallas", "TX"),
    ("W03", "Atlanta DC", "Atlanta", "GA"),
]

carriers = ["UPS", "FedEx", "DHL", "Regional"]

with open(OUT / "products.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id", "product_name", "category", "unit_price"])
    writer.writerows(products)

with open(OUT / "warehouses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["warehouse_id", "warehouse_name", "city", "state"])
    writer.writerows(warehouses)

orders = []
shipments = []
inventory = []

start = datetime(2026, 1, 1)

for i in range(1, 1001):
    order_dt = start + timedelta(
        days=random.randint(0, 120),
        hours=random.randint(0, 23)
    )

    product = random.choice(products)
    warehouse = random.choice(warehouses)

    qty = random.randint(1, 8)
    priority = random.choice(["standard", "expedited", "high"])
    status = random.choice([
        "delivered",
        "delivered",
        "delivered",
        "shipped",
        "backorder"
    ])

    orders.append([
        f"O{i:05d}",
        f"C{random.randint(1, 220):04d}",
        product[0],
        warehouse[0],
        order_dt.isoformat(),
        qty,
        product[3],
        priority,
        status
    ])

    if status != "backorder":
        ship_dt = order_dt + timedelta(hours=random.randint(4, 36))

        planned_days = random.choice([1, 2, 3, 4])

        actual_days = max(
            1,
            planned_days + random.choice([-1, 0, 0, 0, 1, 2])
        )

        delivery_dt = ship_dt + timedelta(days=actual_days)

        shipments.append([
            f"S{i:05d}",
            f"O{i:05d}",
            random.choice(carriers),
            ship_dt.isoformat(),
            delivery_dt.isoformat(),
            planned_days,
            round(random.uniform(5, 45), 2),
            random.randint(50, 1800)
        ])

for day in range(121):
    snapshot_date = (
        start + timedelta(days=day)
    ).date().isoformat()

    for product in products:
        for warehouse in warehouses:
            on_hand = random.randint(0, 300)
            reserved = random.randint(0, min(on_hand, 50))

            inventory.append([
                snapshot_date,
                product[0],
                warehouse[0],
                on_hand,
                reserved
            ])

with open(OUT / "orders.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "order_id",
        "customer_id",
        "product_id",
        "warehouse_id",
        "order_ts",
        "quantity",
        "unit_price",
        "priority",
        "order_status"
    ])

    writer.writerows(orders)

with open(OUT / "shipments.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "shipment_id",
        "order_id",
        "carrier",
        "ship_ts",
        "delivery_ts",
        "planned_delivery_days",
        "transport_cost",
        "distance_miles"
    ])

    writer.writerows(shipments)

with open(OUT / "inventory.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "snapshot_date",
        "product_id",
        "warehouse_id",
        "on_hand_qty",
        "reserved_qty"
    ])

    writer.writerows(inventory)

print("Synthetic supply-chain data generated.")
