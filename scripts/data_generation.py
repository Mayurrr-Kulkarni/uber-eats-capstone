import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and set seeds for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Configuration: Number of records
NUM_CUSTOMERS = 2000
NUM_RESTAURANTS = 150
NUM_DRIVERS = 300
NUM_ORDERS = 15000

def generate_customers():
    print("Generating Customers...")
    zones = ['Downtown', 'North Hills', 'Southside', 'West End', 'East Bay', 'Suburbs']
    data = []
    for i in range(1, NUM_CUSTOMERS + 1):
        age = int(np.random.normal(35, 10))
        age = max(18, min(80, age)) # Bound ages
        data.append({
            'customer_id': f'CUST_{i:05d}',
            'age': age,
            'location_zone': random.choice(zones),
            'lifetime_orders': int(np.random.exponential(15) + 1),
            'account_created': fake.date_between(start_date='-3y', end_date='today')
        })
    return pd.DataFrame(data)

def generate_restaurants():
    print("Generating Restaurants...")
    categories = ['Italian', 'Fast Food', 'Healthy/Vegan', 'Asian', 'Mexican', 'Indian', 'Dessert']
    data = []
    for i in range(1, NUM_RESTAURANTS + 1):
        cat = random.choice(categories)
        # Fast food prep is faster, healthy is slower, etc.
        base_prep = 15 if cat == 'Fast Food' else (25 if cat in ['Italian', 'Healthy/Vegan'] else 20)
        data.append({
            'restaurant_id': f'REST_{i:04d}',
            'name': fake.company(),
            'category': cat,
            'avg_rating': round(np.random.normal(4.2, 0.4), 1),
            'prep_time_mean': round(np.random.normal(base_prep, 3), 1),
            'price_tier': random.choice(['$', '$$', '$$$', '$$$$'])
        })
    # Clip ratings to max 5.0
    df = pd.DataFrame(data)
    df['avg_rating'] = df['avg_rating'].clip(1.0, 5.0)
    return df

def generate_drivers():
    print("Generating Drivers...")
    data = []
    for i in range(1, NUM_DRIVERS + 1):
        data.append({
            'driver_id': f'DRV_{i:04d}',
            'vehicle_type': random.choice(['Bicycle', 'Scooter', 'Sedan', 'SUV']),
            'driver_rating': round(np.random.normal(4.7, 0.2), 1),
            'total_deliveries': int(np.random.exponential(500) + 10)
        })
    df = pd.DataFrame(data)
    df['driver_rating'] = df['driver_rating'].clip(1.0, 5.0)
    return df

def generate_orders(customers, restaurants):
    print("Generating Orders...")
    data = []
    start_date = datetime.now() - timedelta(days=365)
    
    customer_ids = customers['customer_id'].tolist()
    restaurant_ids = restaurants['restaurant_id'].tolist()
    
    for i in range(1, NUM_ORDERS + 1):
        # Time-series pattern: More orders on weekends, higher volume towards end of year
        days_offset = random.randint(0, 365)
        base_time = start_date + timedelta(days=days_offset)
        
        # Hourly pattern: spikes at lunch (12-2) and dinner (6-8)
        hour = int(np.random.choice(
            [10,11,12,13,14,15,16,17,18,19,20,21,22,23], 
            p=[0.02,0.03,0.15,0.15,0.05,0.03,0.04,0.1,0.2,0.15,0.05,0.02,0.005,0.005]
        ))
        minute = random.randint(0, 59)
        order_time = base_time.replace(hour=hour, minute=minute)
        
        # Order Amount pattern: Higher amounts for weekends and specific restaurant categories
        rest_id = random.choice(restaurant_ids)
        base_amount = abs(np.random.normal(25, 15))
        order_amount = max(8.0, round(base_amount, 2))
        
        data.append({
            'order_id': f'ORD_{i:07d}',
            'customer_id': random.choice(customer_ids),
            'restaurant_id': rest_id,
            'order_timestamp': order_time.strftime('%Y-%m-%d %H:%M:%S'),
            'order_amount': order_amount,
            'order_status': np.random.choice(['Completed', 'Cancelled', 'Refunded'], p=[0.94, 0.04, 0.02])
        })
    
    df = pd.DataFrame(data)
    # Sort chronologically for ARIMA/time-series forecasting realism
    return df.sort_values('order_timestamp').reset_index(drop=True)

def generate_deliveries_and_reviews_and_payments(orders, restaurants, drivers):
    print("Generating Deliveries, Reviews, and Payments...")
    deliveries_data = []
    reviews_data = []
    payments_data = []
    
    # NLP Review banks based on sentiment
    positive_reviews = ["Great food!", "Fast delivery.", "Everything was perfect.", "Still hot when it arrived!", "My favorite place."]
    neutral_reviews = ["It was okay.", "Standard food.", "Delivery was a bit slow but food was fine.", "Average experience."]
    negative_reviews = ["Cold food.", "Took way too long.", "Missing items.", "Driver was rude.", "Terrible taste, never again."]
    
    driver_ids = drivers['driver_id'].tolist()
    rest_dict = restaurants.set_index('restaurant_id').to_dict('index')
    
    for idx, row in orders.iterrows():
        status = row['order_status']
        if status != 'Completed':
            continue
            
        order_id = row['order_id']
        rest_id = row['restaurant_id']
        amount = row['order_amount']
        
        # 1. Delivery Generation
        dist = abs(np.random.normal(3.5, 2.0))
        distance_miles = max(0.5, round(dist, 1))
        weather = np.random.choice(['Clear', 'Rain', 'Snow', 'Cloudy'], p=[0.6, 0.2, 0.05, 0.15])
        traffic = np.random.choice(['Light', 'Moderate', 'Heavy'], p=[0.5, 0.3, 0.2])
        
        # Calculate realistic times
        base_prep = rest_dict[rest_id]['prep_time_mean']
        actual_prep = max(5, int(np.random.normal(base_prep, 5)))
        
        # Traffic & Weather impact delivery time
        traffic_mult = 1.5 if traffic == 'Heavy' else (1.2 if traffic == 'Moderate' else 1.0)
        weather_mult = 1.4 if weather in ['Snow', 'Rain'] else 1.0
        actual_transit = int((distance_miles * 5) * traffic_mult * weather_mult)
        
        total_delivery_time = actual_prep + actual_transit
        
        deliveries_data.append({
            'delivery_id': f'DEL_{idx+1:07d}',
            'order_id': order_id,
            'driver_id': random.choice(driver_ids),
            'distance_miles': distance_miles,
            'weather_condition': weather,
            'traffic_condition': traffic,
            'prep_time_mins': actual_prep,
            'transit_time_mins': actual_transit,
            'total_time_mins': total_delivery_time
        })
        
        # 2. Reviews Generation (Pattern: long delivery = lower rating = negative NLP)
        if random.random() < 0.6: # 60% of people leave reviews
            # Calculate dynamic rating based on delivery experience
            rating = 5
            if total_delivery_time > 60: rating -= 2
            elif total_delivery_time > 45: rating -= 1
            if weather_mult > 1.0: rating += 1 # More forgiving in bad weather
            
            rating = max(1, min(5, int(np.random.normal(rating, 0.8))))
            
            if rating >= 4: review_text = random.choice(positive_reviews)
            elif rating == 3: review_text = random.choice(neutral_reviews)
            else: review_text = random.choice(negative_reviews)
            
            reviews_data.append({
                'review_id': f'REV_{idx+1:07d}',
                'order_id': order_id,
                'rating_score': rating,
                'review_text': review_text
            })
            
        # 3. Payments Generation (Pattern: high rating = higher tip)
        base_tip_pct = np.random.normal(0.15, 0.05)
        # Tip suffers if delivery was exceedingly long
        if total_delivery_time > 50: base_tip_pct -= 0.05
        tip_pct = max(0.0, min(0.40, base_tip_pct))
        tip_amount = round(amount * tip_pct, 2)
        
        payments_data.append({
            'payment_id': f'PAY_{idx+1:07d}',
            'order_id': order_id,
            'payment_method': np.random.choice(['Credit Card', 'Apple Pay', 'PayPal', 'Debit Card'], p=[0.5, 0.3, 0.1, 0.1]),
            'subtotal': amount,
            'delivery_fee': round(2.99 + (distance_miles * 0.50), 2),
            'tip_amount': tip_amount,
            'total_charged': round(amount + 2.99 + (distance_miles * 0.50) + tip_amount, 2)
        })

    return pd.DataFrame(deliveries_data), pd.DataFrame(reviews_data), pd.DataFrame(payments_data)

if __name__ == "__main__":
    # Generate Entities
    df_customers = generate_customers()
    df_restaurants = generate_restaurants()
    df_drivers = generate_drivers()
    df_orders = generate_orders(df_customers, df_restaurants)
    
    # Generate Transactional Links
    df_deliveries, df_reviews, df_payments = generate_deliveries_and_reviews_and_payments(
        df_orders, df_restaurants, df_drivers
    )
    
    # Export to CSV
    print("Exporting datasets to CSV...")
    df_customers.to_csv('customers.csv', index=False)
    df_restaurants.to_csv('restaurants.csv', index=False)
    df_drivers.to_csv('drivers.csv', index=False)
    df_orders.to_csv('orders.csv', index=False)
    df_deliveries.to_csv('deliveries.csv', index=False)
    df_reviews.to_csv('reviews.csv', index=False)
    df_payments.to_csv('payments.csv', index=False)
    print("Data generation complete. 7 files saved successfully.")