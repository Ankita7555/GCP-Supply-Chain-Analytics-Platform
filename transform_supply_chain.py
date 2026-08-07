from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")

OUT.mkdir(parents=True, exist_ok=True)

orders = pd.read_csv(RAW / "orders.csv")
shipments = pd.read_csv(RAW / "shipments.csv")
inventory = pd.read_csv(RAW / "inventory.csv")

orders["order_ts"] = pd.to_datetime(
    orders["order_ts"]
)

shipments["ship_ts"] = pd.to_datetime(
    shipments["ship_ts"]
)

shipments["delivery_ts"] = pd.to_datetime(
    shipments["delivery_ts"]
)

# -------------------------
# DATA QUALITY
# -------------------------

orders = orders.drop_duplicates(
    subset=["order_id"]
)

orders = orders[
    orders["quantity"] > 0
]

orders = orders[
    orders["unit_price"] >= 0
]

# -------------------------
# SHIPMENT KPIs
# -------------------------

shipments["actual_delivery_days"] = (
    shipments["delivery_ts"]
    - shipments["ship_ts"]
).dt.total_seconds() / 86400

shipments["is_delayed"] = (
    shipments["actual_delivery_days"]
    > shipments["planned_delivery_days"]
).astype(int)

# -------------------------
# INVENTORY KPI
# -------------------------

inventory["available_qty"] = (
    inventory["on_hand_qty"]
    - inventory["reserved_qty"]
).clip(lower=0)

inventory["stockout_flag"] = (
    inventory["available_qty"] == 0
).astype(int)

orders.to_csv(
    OUT / "orders_clean.csv",
    index=False
)

shipments.to_csv(
    OUT / "shipments_enriched.csv",
    index=False
)

inventory.to_csv(
    OUT / "inventory_enriched.csv",
    index=False
)

print("Transformation complete.")
