import pandas as pd
import numpy as np
import uuid
import json
from datetime import datetime, timedelta
from pathlib import Path

# Inisialisasi Path dan direktori wajib sesuai spesifikasi[cite: 5]
out = Path('data_generator')
out.mkdir(exist_ok=True)

# Menggunakan Random Number Generator modern (seed 42)
rng = np.random.default_rng(42)

# Konfigurasi Volume Minimal (Wajib mengikuti aturan, bukan n=10_000)[cite: 1]
NUM_CUSTOMERS = 50_000
NUM_TRANSACTIONS = 1_000_000
NUM_CLICKSTREAMS = 200_000
DIRTY_RATIO = 0.05

def generate_customers():
    print("Generating customers.csv...")
    customer_ids = [f"CUST-{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)]
    age_groups = rng.choice(['18-24', '25-34', '35-44', '45-54', '55+'], size=NUM_CUSTOMERS)
    genders = rng.choice(['M', 'F'], size=NUM_CUSTOMERS)
    signup_dates = [(datetime(2022, 1, 1) + timedelta(days=int(rng.integers(0, 700)))).strftime('%Y-%m-%d') for _ in range(NUM_CUSTOMERS)]
    tiers = rng.choice(['Basic', 'Silver', 'Gold', 'Platinum'], size=NUM_CUSTOMERS)
    cities = rng.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Makassar'], size=NUM_CUSTOMERS)
    
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'age_group': age_groups,
        'gender': genders,
        'signup_date': signup_dates,
        'membership_tier': tiers,
        'city': cities
    })
    return df, customer_ids

def generate_transactions(customer_ids):
    print("Generating transactions.csv with Veracity Check...")
    txn_ids = [f"TXN-{uuid.uuid4().hex[:8].upper()}" for _ in range(NUM_TRANSACTIONS)]
    cust_ids = rng.choice(customer_ids, size=NUM_TRANSACTIONS)
    
    base_date = datetime(2023, 1, 1)
    timestamps = [base_date + timedelta(minutes=int(rng.integers(0, 1000000))) for _ in range(NUM_TRANSACTIONS)]
    product_ids = [f"PRD-{i:03d}" for i in rng.integers(1, 500, size=NUM_TRANSACTIONS)]
    categories = rng.choice(['Electronics', 'Apparel', 'Home', 'Beauty', 'Sports'], size=NUM_TRANSACTIONS)
    quantities = rng.integers(1, 15, size=NUM_TRANSACTIONS)
    prices = rng.integers(50000, 5000000, size=NUM_TRANSACTIONS)
    discounts = rng.uniform(0, 0.5, size=NUM_TRANSACTIONS).round(2)
    payments = rng.choice(['Credit Card', 'E-Wallet', 'Transfer', 'COD'], size=NUM_TRANSACTIONS)
    cities = rng.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan'], size=NUM_TRANSACTIONS)

    df = pd.DataFrame({
        'transaction_id': txn_ids,
        'customer_id': cust_ids,
        'timestamp': timestamps,
        'product_id': product_ids,
        'category': categories,
        'quantity': quantities,
        'price': prices,
        'discount': discounts,
        'payment_method': payments,
        'city': cities
    })

    # --- ATURAN INJEKSI DATA KOTOR (5% - 10%)[cite: 1] ---
    num_dirty = int(NUM_TRANSACTIONS * DIRTY_RATIO)
    all_indices = df.index.values.copy()
    rng.shuffle(all_indices) # Shuffle untuk mengambil sampel acak
    
    # 1. Missing Values (customer_id, timestamp, category)
    null_idx = all_indices[:num_dirty]
    df.loc[null_idx[:num_dirty//3], 'customer_id'] = np.nan
    df.loc[null_idx[num_dirty//3:2*num_dirty//3], 'timestamp'] = np.nan
    df.loc[null_idx[2*num_dirty//3:], 'category'] = np.nan

    # 2. Inconsistent Formatting (City: Jakarta, JKT, jakarta, DKI Jakarta)
    inconsistent_idx = all_indices[num_dirty:2*num_dirty]
    df.loc[inconsistent_idx, 'city'] = rng.choice(['JKT', 'jakarta', 'DKI Jakarta'], size=num_dirty)

    # 3. Outliers & Invalid Values (Harga negatif & Tanggal masa depan)
    outlier_idx = all_indices[2*num_dirty:3*num_dirty]
    df.loc[outlier_idx[:num_dirty//2], 'price'] = -250000
    df.loc[outlier_idx[num_dirty//2:], 'timestamp'] = datetime(2099, 12, 31)

    # 4. Duplicate Records (Duplikasi transaction_id)
    dup_idx = all_indices[3*num_dirty:4*num_dirty]
    df_duplicates = df.loc[dup_idx].copy()
    df = pd.concat([df, df_duplicates], ignore_index=True) 
    
    return df

def generate_clickstream(customer_ids):
    print("Generating clickstream.json with Veracity Check (Duplicates)...")
    
    # 1. Vektorisasi untuk kecepatan
    user_ids_array = rng.choice(customer_ids, size=NUM_CLICKSTREAMS)
    page_urls_array = rng.choice(['home', 'product', 'cart', 'checkout'], size=NUM_CLICKSTREAMS)
    actions_array = rng.choice(['view', 'click', 'add_to_cart', 'purchase'], size=NUM_CLICKSTREAMS)
    devices_array = rng.choice(['Mobile', 'Desktop', 'Tablet'], size=NUM_CLICKSTREAMS)
    minutes_array = rng.integers(0, 1000000, size=NUM_CLICKSTREAMS)
    
    base_date = datetime(2023, 1, 1)
    records = []
    
    # 2. Loop untuk merangkai dictionary utama
    for i in range(NUM_CLICKSTREAMS):
        record = {
            'session_id': f"SESS-{uuid.uuid4().hex[:8]}", # Ini bertindak sebagai unique identifier
            'user_id': str(user_ids_array[i]),
            'timestamp': (base_date + timedelta(minutes=int(minutes_array[i]))).isoformat(),
            'page_url': f"https://shop.com/{page_urls_array[i]}",
            'action_event': str(actions_array[i]),
            'device_type': str(devices_array[i])
        }
        records.append(record)
    
    # --- ATURAN INJEKSI DATA KOTOR UNTUK JSON (Duplicate Records) ---
    num_dirty_json = int(NUM_CLICKSTREAMS * DIRTY_RATIO)
    
    # Mengambil indeks acak dari records yang sudah ada
    dup_indices = rng.choice(len(records), size=num_dirty_json, replace=False)
    
    # Menyalin (duplikasi) record terpilih dan menambahkannya ke akhir list
    for idx in dup_indices:
        records.append(records[idx].copy())
        
    return records

if __name__ == "__main__":
    df_customers, cust_ids = generate_customers()
    df_transactions = generate_transactions(cust_ids)
    clickstream_data = generate_clickstream(cust_ids)

    # Menggunakan objek `out` dari pathlib
    df_customers.to_csv(out / 'customers.csv', index=False)
    df_transactions.to_csv(out / 'transactions.csv', index=False)
    
    with open(out / 'clickstream.json', 'w') as f:
        for record in clickstream_data:
            f.write(json.dumps(record) + "\n")

    # Cetak list file menggunakan iterdir()
    print('Data dibuat:', sorted(p.name for p in out.iterdir()))