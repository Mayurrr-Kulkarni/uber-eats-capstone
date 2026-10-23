# Uber Eats Synthetic Data Dictionary

This document outlines the schema and underlying relationships for the synthetic Uber Eats relational dataset. The data is designed to support K-Means clustering, NLP sentiment analysis, time-series forecasting (ARIMA), and regression modeling.

## 1. Customers (`customers.csv`)
Demographic and account data for the platform's user base. Includes location clustering targets.
* **`customer_id`** (String): Unique alphanumeric identifier for the customer.
* **`age`** (Integer): Customer age, normally distributed (bounded 18-80).
* **`location_zone`** (String): Geographic area for spatial K-Means clustering.
* **`lifetime_orders`** (Integer): Total historical order count (exponentially distributed).
* **`account_created`** (Date): The date the customer registered on the platform.

## 2. Restaurants (`restaurants.csv`)
Merchant metadata providing categorical features and baseline operational metrics.
* **`restaurant_id`** (String): Unique identifier for the restaurant.
* **`name`** (String): Synthetic company name.
* **`category`** (String): Cuisine type (e.g., Fast Food, Italian, Healthy/Vegan).
* **`avg_rating`** (Float): Historical average customer rating (1.0 to 5.0).
* **`prep_time_mean`** (Float): Baseline average preparation time in minutes, varying by category.
* **`price_tier`** (String): Categorical pricing indicator ($, $$, $$$, $$$$).

## 3. Drivers (`drivers.csv`)
Delivery partner statistics for resource allocation and supply-side modeling.
* **`driver_id`** (String): Unique identifier for the delivery driver.
* **`vehicle_type`** (String): Mode of transport (Bicycle, Scooter, Sedan, SUV).
* **`driver_rating`** (Float): Overall driver rating (1.0 to 5.0).
* **`total_deliveries`** (Integer): Lifetime number of deliveries completed by the driver.

## 4. Orders (`orders.csv`)
The central transaction table linking customers and merchants, enriched with time-series data.
* **`order_id`** (String): Unique identifier for the transaction.
* **`customer_id`** (String): Foreign key referencing `Customers`.
* **`restaurant_id`** (String): Foreign key referencing `Restaurants`.
* **`order_timestamp`** (Datetime): Exact time of order placement. Features seasonal and intraday volume spikes.
* **`order_amount`** (Float): Base cost of the food ordered.
* **`order_status`** (String): Current state of the order (Completed, Cancelled, Refunded).

## 5. Deliveries (`deliveries.csv`)
Logistical data mapped to completed orders, suitable for regression analysis on delivery delays.
* **`delivery_id`** (String): Unique identifier for the delivery leg.
* **`order_id`** (String): Foreign key referencing `Orders`.
* **`driver_id`** (String): Foreign key referencing `Drivers`.
* **`distance_miles`** (Float): Geographical distance from restaurant to customer.
* **`weather_condition`** (String): Categorical weather state (Clear, Rain, Snow, Cloudy).
* **`traffic_condition`** (String): Traffic severity multiplier (Light, Moderate, Heavy).
* **`prep_time_mins`** (Integer): Actual time taken by the restaurant to prepare the specific order.
* **`transit_time_mins`** (Integer): Drive time, mathematically inflated by adverse weather and heavy traffic.
* **`total_time_mins`** (Integer): Total elapsed time from order placement to delivery.

## 6. Reviews (`reviews.csv`)
Customer feedback strings and discrete scores for NLP sentiment modeling. Rating degrades dynamically based on `total_time_mins`.
* **`review_id`** (String): Unique identifier for the review.
* **`order_id`** (String): Foreign key referencing `Orders`.
* **`rating_score`** (Integer): Score out of 5 for this specific transaction.
* **`review_text`** (String): Textual review corresponding to the assigned sentiment score.

## 7. Payments (`payments.csv`)
Financial breakdown of the order, containing dynamic correlations (e.g., tipping percentage drops on delayed deliveries).
* **`payment_id`** (String): Unique identifier for the payment transaction.
* **`order_id`** (String): Foreign key referencing `Orders`.
* **`payment_method`** (String): Transaction medium (Credit Card, Apple Pay, etc.).
* **`subtotal`** (Float): Mirror of `order_amount`.
* **`delivery_fee`** (Float): Dynamic fee calculated as a base rate plus a per-mile modifier.
* **`tip_amount`** (Float): Gratuity, positively correlated with fast delivery and high ratings.
* **`total_charged`** (Float): The absolute total charged to the customer.