"""Generate small sample datasets for PySpark practice.

Run once before working through the notebooks/exercises:
    python scripts/generate_data.py

Creates CSVs in data/generated/ (~50k rows total, a few MB).
Pure standard library — no dependencies needed.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "generated"

CITIES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
    ("Seattle", "WA"),
]

PRODUCTS = [
    (1, "Laptop", "Electronics", 899.99),
    (2, "Headphones", "Electronics", 149.50),
    (3, "Coffee Maker", "Home", 79.00),
    (4, "Desk Chair", "Furniture", 210.00),
    (5, "Monitor", "Electronics", 299.99),
    (6, "Blender", "Home", 55.25),
    (7, "Bookshelf", "Furniture", 120.00),
    (8, "Keyboard", "Electronics", 89.99),
    (9, "Lamp", "Home", 34.50),
    (10, "Standing Desk", "Furniture", 450.00),
]

FIRST_NAMES = ["Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace",
               "Henry", "Isla", "Jack", "Kira", "Liam", "Maya", "Noah", "Priya"]
LAST_NAMES = ["Smith", "Johnson", "Lee", "Patel", "Garcia", "Brown", "Chen",
              "Davis", "Kim", "Lopez", "Nguyen", "Wilson"]


def write_csv(name: str, header: list[str], rows: list) -> None:
    path = OUT_DIR / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # customers.csv — includes some messy data on purpose (nulls, casing)
    n_customers = 2_000
    customers = []
    for cid in range(1, n_customers + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        city, state = random.choice(CITIES)
        email = f"{first.lower()}.{last.lower()}{cid}@example.com"
        # ~5% missing emails, ~5% inconsistent city casing (cleaning practice)
        if random.random() < 0.05:
            email = ""
        if random.random() < 0.05:
            city = city.upper()
        signup = date(2022, 1, 1) + timedelta(days=random.randint(0, 1200))
        customers.append([cid, first, last, email, city, state, signup.isoformat()])
    write_csv("customers.csv",
              ["customer_id", "first_name", "last_name", "email", "city", "state", "signup_date"],
              customers)

    # products.csv
    write_csv("products.csv",
              ["product_id", "product_name", "category", "unit_price"],
              [list(p) for p in PRODUCTS])

    # orders.csv — the big one, for aggregations/joins/window functions
    n_orders = 50_000
    orders = []
    for oid in range(1, n_orders + 1):
        cid = random.randint(1, n_customers)
        pid, _, _, price = random.choice(PRODUCTS)
        qty = random.randint(1, 5)
        # ~2% orders reference a nonexistent customer (join practice)
        if random.random() < 0.02:
            cid = n_customers + random.randint(1, 100)
        order_date = date(2023, 1, 1) + timedelta(days=random.randint(0, 900))
        discount = random.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.20])
        total = round(price * qty * (1 - discount), 2)
        orders.append([oid, cid, pid, qty, discount, total, order_date.isoformat()])
    write_csv("orders.csv",
              ["order_id", "customer_id", "product_id", "quantity", "discount", "order_total", "order_date"],
              orders)

    print("\nDone. Datasets are in data/generated/")


if __name__ == "__main__":
    main()
