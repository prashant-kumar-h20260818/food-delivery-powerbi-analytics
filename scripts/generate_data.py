"""
Rebuild the synthetic portfolio dataset.

This script intentionally generates fictional food-delivery data at the same
portfolio scale used by the Power BI report:
- 200,000 orders
- 20,000 customers
- 56,000 restaurant registries
- ₹164,914,000 generated revenue
- 50.28% repeat customers
- 48.12% late-order rate
- 10.00% cancellation rate

Run:
    python scripts/generate_data.py
"""

from pathlib import Path
import numpy as np
import pandas as pd
import json

SEED = 42
N_ORDERS = 200_000
N_CUSTOMERS = 20_000
N_RESTAURANTS = 56_000
TARGET_REVENUE = 164_914_000.00
TARGET_REPEAT_CUSTOMERS = 10_056
TARGET_LATE_ORDERS = 96_240
TARGET_CANCELLED = 20_000
TARGET_DELIVERED = 160_220
TARGET_REFUNDED = N_ORDERS - TARGET_CANCELLED - TARGET_DELIVERED

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VALIDATION = ROOT / "validation"
DATA.mkdir(exist_ok=True)
VALIDATION.mkdir(exist_ok=True)

rng = np.random.default_rng(SEED)

cities = ["Bengaluru", "Delhi", "Mumbai", "Hyderabad", "Pune", "Chennai", "Kolkata", "Gurugram"]
city_weights = np.array([0.25, 0.15, 0.14, 0.12, 0.11, 0.09, 0.08, 0.06], dtype=float)
city_weights /= city_weights.sum()
areas_by_city = {
    "Bengaluru": ["BTM", "Koramangala 5th Block", "HSR", "Indiranagar", "Whitefield"],
    "Delhi": ["Connaught Place", "Saket", "Dwarka", "Rohini", "Hauz Khas"],
    "Mumbai": ["Andheri", "Bandra", "Powai", "Lower Parel", "Borivali"],
    "Hyderabad": ["Gachibowli", "Hitech City", "Banjara Hills", "Kondapur", "Madhapur"],
    "Pune": ["Viman Nagar", "Hinjewadi", "Kothrud", "Baner", "Wakad"],
    "Chennai": ["T Nagar", "Velachery", "Anna Nagar", "OMR", "Adyar"],
    "Kolkata": ["Salt Lake", "Park Street", "New Town", "Ballygunge", "Howrah"],
    "Gurugram": ["Cyber City", "Sector 29", "Golf Course Road", "Sohna Road", "Udyog Vihar"],
}
cuisines = [
    "North Indian", "Chinese", "South Indian", "Fast Food", "Biryani", "Desserts",
    "Continental", "Street Food", "Cafe", "Italian", "Mughlai", "Healthy Food"
]

# ---------- Restaurants ----------
restaurant_ids = np.array([f"R{i:06d}" for i in range(1, N_RESTAURANTS + 1)])
restaurant_city = rng.choice(cities, N_RESTAURANTS, p=city_weights)
restaurant_area = np.array([rng.choice(areas_by_city[c]) for c in restaurant_city])
cost_bucket = rng.choice(["Budget", "Mid Range", "Premium"], N_RESTAURANTS, p=[0.58, 0.30, 0.12])

cost_for_two = np.empty(N_RESTAURANTS, dtype=int)
for bucket, lo, hi in [("Budget",250,601),("Mid Range",650,1501),("Premium",1600,3501)]:
    mask = cost_bucket == bucket
    cost_for_two[mask] = rng.integers(lo, hi, mask.sum())

ratings = np.clip(rng.normal(3.70, 0.48, N_RESTAURANTS), 1.8, 4.9)
ratings = np.clip(ratings + (3.70 - ratings.mean()), 1.8, 4.9)
ratings = np.round(ratings, 2)
votes = np.clip(rng.gamma(2.0, 130.5, N_RESTAURANTS), 0, 2500).astype(int)
primary_cuisine = rng.choice(
    cuisines, N_RESTAURANTS,
    p=[0.20,0.14,0.10,0.10,0.09,0.07,0.07,0.06,0.05,0.05,0.04,0.03]
)

restaurants = pd.DataFrame({
    "RestaurantID": restaurant_ids,
    "RestaurantName": [f"QuickBite Kitchen {i:05d}" for i in range(1, N_RESTAURANTS + 1)],
    "City": restaurant_city,
    "Area": restaurant_area,
    "PrimaryCuisine": primary_cuisine,
    "CostBucket": cost_bucket,
    "CostForTwo": cost_for_two,
    "Rating": ratings,
    "Votes": votes,
    "OnlineDelivery": rng.choice(["Yes","No"], N_RESTAURANTS, p=[0.82,0.18]),
    "TableBooking": rng.choice(["Yes","No"], N_RESTAURANTS, p=[0.28,0.72]),
})

# ---------- Customers ----------
customer_ids = np.array([f"C{i:06d}" for i in range(1, N_CUSTOMERS + 1)])
counts = np.ones(N_CUSTOMERS, dtype=int)
repeat_idx = rng.choice(N_CUSTOMERS, TARGET_REPEAT_CUSTOMERS, replace=False)
counts[repeat_idx] += 1
remaining = N_ORDERS - counts.sum()
w = rng.lognormal(0.0, 0.9, TARGET_REPEAT_CUSTOMERS)
w /= w.sum()
counts[repeat_idx] += rng.multinomial(remaining, w)

signup_start = np.datetime64("2022-01-01")
signup_end = np.datetime64("2025-07-31")
signup_dates = signup_start + rng.integers(
    0, int((signup_end - signup_start).astype(int)) + 1, N_CUSTOMERS
).astype("timedelta64[D]")

customers = pd.DataFrame({
    "CustomerID": customer_ids,
    "SignupDate": pd.to_datetime(signup_dates),
    "HomeCity": rng.choice(cities, N_CUSTOMERS, p=city_weights),
    "AgeBand": rng.choice(["18-24","25-34","35-44","45-54","55+"], N_CUSTOMERS, p=[0.16,0.37,0.25,0.14,0.08]),
    "PreferredChannel": rng.choice(["Mobile App","Web"], N_CUSTOMERS, p=[0.88,0.12]),
})

order_customer = np.repeat(customer_ids, counts)
rng.shuffle(order_customer)

# ---------- Orders ----------
order_ids = np.array([f"O{i:07d}" for i in range(1, N_ORDERS + 1)])

bucket_counts = {"Budget":118_200, "Mid Range":57_020, "Premium":24_780}
order_buckets = np.concatenate([np.repeat(k, v) for k, v in bucket_counts.items()])
rng.shuffle(order_buckets)

rest_pool = {b: np.where(cost_bucket == b)[0] for b in bucket_counts}
rest_idx = np.empty(N_ORDERS, dtype=int)
for b in bucket_counts:
    pos = np.where(order_buckets == b)[0]
    rest_idx[pos] = rng.choice(rest_pool[b], len(pos), replace=True)

order_restaurant = restaurant_ids[rest_idx]
order_city = restaurant_city[rest_idx]
order_area = restaurant_area[rest_idx]
order_cuisine = primary_cuisine[rest_idx]

dates = pd.date_range("2023-01-01", "2025-07-31", freq="D")
date_weights = np.ones(len(dates), dtype=float)
date_weights += np.where(dates.dayofweek >= 5, 0.25, 0)
date_weights += np.where(pd.Series(dates.month).isin([10,11,12]).to_numpy(), 0.12, 0)
date_weights *= np.linspace(0.90, 1.10, len(dates))
date_weights /= date_weights.sum()
order_dates = rng.choice(dates.to_numpy(), N_ORDERS, p=date_weights)

hour_probs = np.array([
    0.01,0.005,0.003,0.002,0.002,0.003,0.008,0.02,0.04,0.05,0.05,0.06,
    0.08,0.08,0.06,0.04,0.04,0.05,0.08,0.10,0.09,0.07,0.04,0.02
], dtype=float)
hour_probs /= hour_probs.sum()
hours = rng.choice(np.arange(24), N_ORDERS, p=hour_probs)
minutes = rng.integers(0, 60, N_ORDERS)
order_dt = pd.to_datetime(order_dates) + pd.to_timedelta(hours, unit="h") + pd.to_timedelta(minutes, unit="m")

raw_amount = np.empty(N_ORDERS)
for b, mean, sd in [("Budget",560,180),("Mid Range",980,260),("Premium",1750,450)]:
    pos = np.where(order_buckets == b)[0]
    raw_amount[pos] = np.clip(rng.normal(mean, sd, len(pos)), 120, None)
amounts = np.round(raw_amount * (TARGET_REVENUE / raw_amount.sum()), 2)
amounts[-1] = round(amounts[-1] + (TARGET_REVENUE - amounts.sum()), 2)

cancel_risk_factor = {
    "Bengaluru":0.9, "Delhi":1.1, "Mumbai":1.2, "Hyderabad":0.95,
    "Pune":0.9, "Chennai":0.92, "Kolkata":1.05, "Gurugram":1.08
}
cancel_score = np.array([cancel_risk_factor[c] for c in order_city]) * rng.random(N_ORDERS)
cancel_idx = np.argpartition(cancel_score, -TARGET_CANCELLED)[-TARGET_CANCELLED:]
remaining_mask = np.ones(N_ORDERS, dtype=bool)
remaining_mask[cancel_idx] = False
remaining_idx = np.where(remaining_mask)[0]
refund_idx = rng.choice(remaining_idx, TARGET_REFUNDED, replace=False)

status = np.full(N_ORDERS, "Delivered", dtype=object)
status[cancel_idx] = "Cancelled"
status[refund_idx] = "Refunded"

noncancel = status != "Cancelled"
delivery = np.round(np.clip(rng.normal(44.55, 14.5, noncancel.sum()), 12, 110), 2)
target_sum = 44.55 * noncancel.sum()
delivery[-1] = round(delivery[-1] + (target_sum - delivery.sum()), 2)
delivery_minutes = np.full(N_ORDERS, np.nan)
delivery_minutes[noncancel] = delivery

late_factor = {
    "Bengaluru":0.95, "Delhi":1.03, "Mumbai":1.16, "Hyderabad":0.98,
    "Pune":0.90, "Chennai":0.92, "Kolkata":1.08, "Gurugram":1.05
}
eligible = np.where(noncancel)[0]
late_score = np.array([late_factor[c] for c in order_city[eligible]]) * (0.4 + rng.random(len(eligible)))
local = np.argpartition(late_score, -TARGET_LATE_ORDERS)[-TARGET_LATE_ORDERS:]
is_late = np.zeros(N_ORDERS, dtype=int)
is_late[eligible[local]] = 1

orders = pd.DataFrame({
    "OrderID": order_ids,
    "OrderDateTime": order_dt,
    "OrderDate": pd.to_datetime(order_dt).date,
    "OrderHour": pd.to_datetime(order_dt).hour,
    "CustomerID": order_customer,
    "RestaurantID": order_restaurant,
    "City": order_city,
    "Area": order_area,
    "PrimaryCuisine": order_cuisine,
    "CostBucket": order_buckets,
    "OrderAmount": amounts,
    "OrderStatus": status,
    "DeliveryMinutes": delivery_minutes,
    "IsLate": is_late,
    "DeliveryDistanceKM": np.round(np.clip(rng.gamma(2.0,2.0,N_ORDERS),0.4,18),2),
    "PaymentMethod": rng.choice(["UPI","Credit Card","Debit Card","Cash","Wallet"], N_ORDERS, p=[0.52,0.18,0.11,0.10,0.09]),
    "OrderChannel": rng.choice(["Mobile App","Web"], N_ORDERS, p=[0.90,0.10]),
    "CustomerRating": np.where(
        status == "Cancelled",
        rng.choice([1,2,3], N_ORDERS, p=[0.55,0.35,0.10]),
        rng.choice([1,2,3,4,5], N_ORDERS, p=[0.03,0.06,0.15,0.36,0.40])
    )
})

cust = orders.groupby("CustomerID").agg(
    LifetimeRevenue=("OrderAmount","sum"),
    LifetimeOrders=("OrderID","count")
).reset_index()
premium_threshold = cust.loc[cust["LifetimeOrders"] > 1, "LifetimeRevenue"].quantile(0.80)
cust["CustomerSegment"] = np.where(
    cust["LifetimeOrders"] == 1,
    "New",
    np.where(cust["LifetimeRevenue"] >= premium_threshold, "Premium", "Returning")
)
customers = customers.merge(cust, on="CustomerID", how="left")
customers["LifetimeRevenue"] = customers["LifetimeRevenue"].round(2)

orders.to_csv(DATA / "orders.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
customers.to_csv(DATA / "customers.csv", index=False, date_format="%Y-%m-%d")
restaurants.to_csv(DATA / "restaurants.csv", index=False)

metrics = {
    "orders": len(orders),
    "customers": customers["CustomerID"].nunique(),
    "restaurants": restaurants["RestaurantID"].nunique(),
    "total_revenue": round(float(orders["OrderAmount"].sum()), 2),
    "aov": round(float(orders["OrderAmount"].mean()), 2),
    "cities": orders["City"].nunique(),
    "cuisines": orders["PrimaryCuisine"].nunique(),
    "delivered_orders": int((orders["OrderStatus"] == "Delivered").sum()),
    "cancelled_orders": int((orders["OrderStatus"] == "Cancelled").sum()),
    "late_orders": int(orders["IsLate"].sum()),
    "late_pct": round(float(orders["IsLate"].mean() * 100), 2),
    "avg_delivery_minutes": round(float(orders.loc[noncancel, "DeliveryMinutes"].mean()), 2),
    "repeat_customers": int((customers["LifetimeOrders"] > 1).sum()),
    "repeat_customer_pct": round(float((customers["LifetimeOrders"] > 1).mean() * 100), 2),
}
with open(VALIDATION / "metrics_summary.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print(json.dumps(metrics, indent=2))
