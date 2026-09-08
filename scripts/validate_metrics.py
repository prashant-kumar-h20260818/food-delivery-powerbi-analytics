from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
metrics = json.loads((ROOT / "validation" / "metrics_summary.json").read_text())

expected = {
    "orders": 200000,
    "customers": 20000,
    "restaurants": 56000,
    "total_revenue": 164914000.0,
    "aov": 824.57,
    "late_orders": 96240,
    "repeat_customers": 10056,
}

for key, value in expected.items():
    actual = metrics.get(key)
    if actual != value:
        raise AssertionError(f"{key}: expected {value}, got {actual}")

print("Validation passed:", expected)
