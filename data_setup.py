import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def reset_data():
    print("⚙️ Initializing Operations Database...")
    
    # 1. TRANSACTION DATA (For Warehouse Layout)
    # Simulating 500 past baskets
    items = ['Milk', 'Bread', 'Eggs', 'Butter', 'Jam', 'Coke', 'Chips', 'Batter', 'Curd']
    data = []
    for _ in range(500):
        # Create correlated baskets (e.g., Milk+Bread)
        basket_size = np.random.randint(1, 5)
        basket = np.random.choice(items, basket_size, replace=False).tolist()
        if 'Milk' in basket and np.random.random() > 0.3: basket.append('Bread')
        if 'Batter' in basket and np.random.random() > 0.3: basket.append('Curd')
        for item in basket:
            data.append({'transaction_id': _, 'item': item})
    pd.DataFrame(data).to_csv('transactions.csv', index=False)

    # 2. LIVE ORDER STREAM (For Logistics)
    # Simulating active orders waiting for dispatch
    orders = [
        {'id': 'ORD-101', 'x': 2, 'y': 3, 'sla': 15, 'status': 'Pending'},
        {'id': 'ORD-102', 'x': 8, 'y': 8, 'sla': 25, 'status': 'Pending'},
        {'id': 'ORD-103', 'x': 3, 'y': 2, 'sla': 12, 'status': 'Pending'},
        {'id': 'ORD-104', 'x': 7, 'y': 9, 'sla': 30, 'status': 'Pending'},
    ]
    pd.DataFrame(orders).to_csv('orders.csv', index=False)

    # 3. INVENTORY SNAPSHOT (For Expiry)
    inventory = [
        {'sku': 'Fresh Milk', 'stock': 45, 'days_to_expiry': 1, 'price': 30},
        {'sku': 'Idli Batter', 'stock': 12, 'days_to_expiry': 4, 'price': 50},
        {'sku': 'Paneer', 'stock': 80, 'days_to_expiry': 2, 'price': 120},
        {'sku': 'Coke Can', 'stock': 150, 'days_to_expiry': 180, 'price': 40},
        {'sku': 'Brown Bread', 'stock': 5, 'days_to_expiry': 1, 'price': 45},
    ]
    pd.DataFrame(inventory).to_csv('inventory.csv', index=False)
    
    print("✅ Database Created: transactions.csv, orders.csv, inventory.csv")

if __name__ == "__main__":
    reset_data()