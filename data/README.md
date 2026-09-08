# Data

The full synthetic dataset is generated locally and intentionally not committed to keep the repository lightweight.

Run from the repository root:

```bash
pip install -r requirements.txt
python scripts/generate_data.py
```

The generator creates:

- `orders.csv` — 200,000 orders
- `customers.csv` — 20,000 customers
- `restaurants.csv` — 56,000 restaurant registries

Expected business totals are recorded in `validation/metrics_summary.json` and `validation/VALIDATION.md`.

All records are fictional and generated for portfolio/learning use.
