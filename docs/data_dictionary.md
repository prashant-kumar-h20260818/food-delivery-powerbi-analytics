# Data Dictionary

## Orders (Fact)
| Column | Type | Description |
|---|---|---|
| OrderID | Text | Unique order identifier |
| OrderDateTime | DateTime | Order timestamp |
| OrderDate | Date | Date used for Date relationship |
| OrderHour | Integer | Hour of day (0-23) |
| CustomerID | Text | Foreign key to Customers |
| RestaurantID | Text | Foreign key to Restaurants |
| City | Text | Restaurant/order city |
| Area | Text | Locality/area |
| PrimaryCuisine | Text | Main cuisine category |
| CostBucket | Text | Budget / Mid Range / Premium |
| OrderAmount | Decimal | Gross order value |
| OrderStatus | Text | Delivered / Cancelled / Refunded |
| DeliveryMinutes | Decimal | Delivery duration; blank for cancelled orders |
| IsLate | Integer | 1 = late, 0 = not late |
| DeliveryDistanceKM | Decimal | Approx. delivery distance |
| PaymentMethod | Text | UPI / card / cash / wallet |
| OrderChannel | Text | Mobile App / Web |
| CustomerRating | Integer | Post-order rating from 1 to 5 |

## Customers (Dimension)
| Column | Type | Description |
|---|---|---|
| CustomerID | Text | Unique customer identifier |
| SignupDate | Date | Customer registration date |
| HomeCity | Text | Customer home city |
| AgeBand | Text | Age band |
| PreferredChannel | Text | Preferred ordering channel |
| LifetimeRevenue | Decimal | Generated lifetime spend |
| LifetimeOrders | Integer | Number of orders |
| CustomerSegment | Text | New / Returning / Premium |

## Restaurants (Dimension)
| Column | Type | Description |
|---|---|---|
| RestaurantID | Text | Unique restaurant identifier |
| RestaurantName | Text | Fictional restaurant name |
| City | Text | City |
| Area | Text | Locality |
| PrimaryCuisine | Text | Cuisine category |
| CostBucket | Text | Budget / Mid Range / Premium |
| CostForTwo | Decimal | Typical cost for two |
| Rating | Decimal | Restaurant rating |
| Votes | Integer | Rating vote count |
| OnlineDelivery | Text | Yes / No |
| TableBooking | Text | Yes / No |

## Date (Dimension)
Created in Power Query using `powerbi/power_query_date.m`.
