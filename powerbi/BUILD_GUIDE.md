# Power BI Dashboard Build Guide

## 0. Generate the data
From the repository root, run:

```bash
pip install -r requirements.txt
python scripts/generate_data.py
```

This creates `data/orders.csv`, `data/customers.csv`, and `data/restaurants.csv` at the full portfolio scale.

## 1. Create the file
Create a new Power BI Desktop file and save it as `FoodDeliveryAnalytics.pbix` in the repository root.

## 2. Create parameter
In Power Query, create a **Text** parameter called `DataFolder`.
Set it to the full local path of this repository's `data` folder.

## 3. Load queries
Create four blank queries and paste the corresponding M scripts:
- `Orders` → `powerbi/power_query_orders.m`
- `Customers` → `powerbi/power_query_customers.m`
- `Restaurants` → `powerbi/power_query_restaurants.m`
- `Date` → `powerbi/power_query_date.m`

The supplied M scripts contain **30+ named ETL/model-preparation steps** across the four queries.

## 4. Model
Create:
- Customers[CustomerID] 1:* Orders[CustomerID]
- Restaurants[RestaurantID] 1:* Orders[RestaurantID]
- Date[Date] 1:* Orders[OrderDate]

Use single-direction filtering and mark Date as a Date table.

## 5. Measures
Create a blank table named `Measures` and add all **21 measures** from `powerbi/dax_measures.dax`.

Recommended formatting:
- Revenue/AOV/Revenue per Restaurant → Currency (₹), 2 decimals
- Percent measures → Percentage, 2 decimals
- Delivery time → Decimal, 2 decimals
- Count measures → Whole number

## 6. Apply theme
View → Themes → Browse for themes → select `powerbi/theme.json`.

# Page 1 — Executive Overview
### KPI cards
- Total Revenue
- Total Orders
- Average Order Value
- Total Customers
- Avg Delivery Time

### Visuals
- Line chart: Date[YearMonth] vs Total Revenue
- Clustered bar: Orders[City] vs Total Revenue
- Donut: Orders[OrderStatus] vs Total Orders
- Bar: Orders[PrimaryCuisine] vs Total Orders
- Matrix: RestaurantName, Total Revenue, Total Orders, Average Rating
- Slicers: Date[Year], Orders[City], Orders[CostBucket]

# Page 2 — Customer Analytics
### KPI cards
- Total Customers
- Repeat Customers
- Repeat Customer %
- Orders per Customer

### Visuals
- Donut: Customers[CustomerSegment] vs Total Customers
- Column chart: Customers[HomeCity] vs Total Customers
- Column chart: Customers[AgeBand] vs Total Revenue
- Line chart: Customers[SignupDate] vs Total Customers
- Table: CustomerID, LifetimeOrders, LifetimeRevenue, CustomerSegment

# Page 3 — Restaurant Performance
### KPI cards
- Total Restaurants
- Average Rating
- Average Votes
- Revenue per Restaurant

### Visuals
- Bar: PrimaryCuisine vs Total Orders
- Scatter: Rating vs Total Revenue; Size = Total Orders; Details = RestaurantName
- Column: CostBucket vs Total Orders
- Bar: RestaurantName vs Total Revenue (Top N = 10)
- Slicers: OnlineDelivery, TableBooking, City

# Page 4 — Delivery & Operations
### KPI cards
- Avg Delivery Time
- Late Orders
- Late Delivery %
- Cancelled Orders
- Cancel %

### Visuals
- Line: Date[YearMonth] vs Avg Delivery Time
- Bar: City vs Late Delivery %
- Bar: City vs Cancelled Orders
- Donut: DeliveryPerformance vs Total Orders
- Scatter: DeliveryDistanceKM vs DeliveryMinutes
- Matrix: City, Total Orders, Delivered Orders, Cancelled Orders, Late Orders

# Page 5 — Advanced Insights
Create a Power BI **Field Parameter** with:
- Total Revenue
- Total Orders
- Average Order Value
- Avg Delivery Time

Use it in a dynamic time-series visual.

Add:
- Decomposition Tree: Total Revenue → City → CostBucket → PrimaryCuisine
- Q&A visual
- Revenue vs Rating scatter
- Drill-down hierarchy: Year → Quarter → Month
- Tooltip page for city-level KPI detail

# Page 6 — Restaurant Details (Drill-through)
Set `Restaurants[RestaurantName]` as the drill-through field.

### Cards
- Total Revenue
- Total Orders
- Average Rating
- Avg Delivery Time

### Visuals
- Order status donut
- Customer segment breakdown
- Monthly revenue trend
- Cuisine/cost context
- Delivery-performance breakdown

Add a Back button.

# Validation Targets
After loading the supplied generated data, the unfiltered report should show approximately/exactly:

- **Orders:** 200,000
- **Customers:** 20,000
- **Restaurants:** 56,000
- **Revenue:** ₹164,914,000.00
- **AOV:** ₹824.57
- **Repeat Customers:** 10,056
- **Repeat Customer %:** 50.28%
- **Late Orders:** 96,240
- **Late Delivery %:** 48.12%
- **Cancelled Orders:** 20,000
- **Average Delivery Time:** 44.55 minutes

## Final Power BI-specific step
This repository contains all data-generation logic, transformations, DAX, theme, model specification, and page specifications.
The `.pbix` binary itself must be created/saved using Microsoft Power BI Desktop.
