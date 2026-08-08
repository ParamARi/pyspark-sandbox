"""Generate messy / semi-structured files for parsing practice.

Run from the project root:
    python scripts/generate_unstructured_data.py

Writes to data/generated/:
  - events.jsonl          Nested JSON lines (clickstream-style)
  - app.log               Free-text log lines with irregular fields
  - support_tickets.csv   CSV with free-text + pipe-delimited tags
"""

from __future__ import annotations

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(7)

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "generated"

PAGES = ["/", "/products", "/cart", "/checkout", "/help", "/account"]
DEVICES = ["desktop", "mobile", "tablet"]
BROWSERS = ["chrome", "safari", "firefox", "edge"]
LEVELS = ["INFO", "WARN", "ERROR"]
SERVICES = ["api", "auth", "payments", "catalog"]
TICKET_SUBJECTS = [
    "Can't reset password",
    "Order never arrived",
    "Charged twice",
    "App crashes on checkout",
    "Wrong item shipped",
    "Refund status?",
]
TAG_POOL = ["billing", "shipping", "login", "bug", "urgent", "refund", "mobile", "vip"]


def write_events(n: int = 2_000) -> None:
    path = OUT_DIR / "events.jsonl"
    start = datetime(2024, 6, 1, 9, 0, 0)
    with path.open("w", encoding="utf-8") as f:
        for i in range(1, n + 1):
            ts = start + timedelta(seconds=random.randint(0, 30 * 24 * 3600))
            # ~8% records are "dirty": missing user, or nested fields as strings
            user_id = None if random.random() < 0.08 else random.randint(1, 500)
            event = {
                "event_id": f"evt-{i:05d}",
                "ts": ts.isoformat() + "Z",
                "user": {"id": user_id, "session": f"s-{random.randint(1000, 9999)}"},
                "page": random.choice(PAGES),
                "device": {
                    "type": random.choice(DEVICES),
                    "browser": random.choice(BROWSERS),
                },
                "props": {
                    "referrer": random.choice(["google", "direct", "email", "ads"]),
                    "cart_value": round(random.uniform(0, 400), 2)
                    if random.random() < 0.35
                    else None,
                },
            }
            if random.random() < 0.05:
                # occasionally bury a JSON object inside a string (real-world mess)
                event["props"] = json.dumps(event["props"])
            f.write(json.dumps(event) + "\n")
    print(f"wrote {path} ({n} lines)")


def write_app_log(n: int = 1_500) -> None:
    path = OUT_DIR / "app.log"
    start = datetime(2024, 7, 1, 0, 0, 0)
    lines = []
    for i in range(n):
        ts = start + timedelta(seconds=random.randint(0, 14 * 24 * 3600))
        level = random.choices(LEVELS, weights=[0.7, 0.2, 0.1])[0]
        service = random.choice(SERVICES)
        req_id = f"req-{random.randint(100000, 999999)}"
        latency = random.randint(12, 2500)
        status = random.choices([200, 201, 400, 401, 404, 500], weights=[70, 5, 8, 5, 7, 5])[0]
        msg = {
            "INFO": f"handled request status={status} latency_ms={latency}",
            "WARN": f"slow request status={status} latency_ms={latency} threshold_ms=800",
            "ERROR": f"request failed status={status} latency_ms={latency} err=timeout",
        }[level]
        # Two slightly different formats on purpose
        if random.random() < 0.6:
            line = f"{ts.strftime('%Y-%m-%d %H:%M:%S')} [{level}] service={service} request_id={req_id} {msg}"
        else:
            line = f"{ts.isoformat()}Z level={level} svc={service} rid={req_id} {msg}"
        lines.append(line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {path} ({n} lines)")


def write_tickets(n: int = 800) -> None:
    path = OUT_DIR / "support_tickets.csv"
    start = datetime(2024, 1, 1)
    rows = []
    for tid in range(1, n + 1):
        created = start + timedelta(days=random.randint(0, 200), hours=random.randint(0, 23))
        subject = random.choice(TICKET_SUBJECTS)
        tags = "|".join(random.sample(TAG_POOL, k=random.randint(1, 3)))
        # free-text body with embedded key=value crumbs
        customer_id = random.randint(1, 2000)
        order_id = random.randint(1, 50000) if random.random() < 0.7 else ""
        body = (
            f"Customer reported: {subject.lower()}. "
            f"customer_id={customer_id} "
            + (f"order_id={order_id} " if order_id else "")
            + f"channel={random.choice(['email', 'chat', 'phone'])}."
        )
        # ~10% missing tags
        if random.random() < 0.1:
            tags = ""
        rows.append([tid, created.isoformat(), subject, tags, body])

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ticket_id", "created_at", "subject", "tags", "body"])
        writer.writerows(rows)
    print(f"wrote {path} ({n} rows)")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_events()
    write_app_log()
    write_tickets()
    print("\nDone. Unstructured practice files are in data/generated/")


if __name__ == "__main__":
    main()
