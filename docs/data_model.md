# Data Model

Use a star schema with single-direction relationships from dimensions to the fact table.

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : "CustomerID"
    RESTAURANTS ||--o{ ORDERS : "RestaurantID"
    DATE ||--o{ ORDERS : "Date -> OrderDate"

    CUSTOMERS {
        text CustomerID PK
        date SignupDate
        text HomeCity
        text CustomerSegment
    }

    RESTAURANTS {
        text RestaurantID PK
        text City
        text PrimaryCuisine
        text CostBucket
        decimal Rating
    }

    DATE {
        date Date PK
        int Year
        text Quarter
        text Month
    }

    ORDERS {
        text OrderID PK
        date OrderDate
        text CustomerID FK
        text RestaurantID FK
        decimal OrderAmount
        text OrderStatus
        decimal DeliveryMinutes
        int IsLate
    }
```

## Relationships
1. `Customers[CustomerID]` (1) → `Orders[CustomerID]` (*)
2. `Restaurants[RestaurantID]` (1) → `Orders[RestaurantID]` (*)
3. `Date[Date]` (1) → `Orders[OrderDate]` (*)

Set all three relationships to **Single** cross-filter direction.
Mark `Date` as the model's date table using `Date[Date]`.
