import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

# Database connection details
DB_USER = "smilex"
DB_PASSWORD = "smilex"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ecommerce_db"
TABLE_NAME = "transactions"

# Load dataset
file_path = "original_data/Fraudulent_E-Commerce_Transaction_Data.csv"
df = pd.read_csv(file_path)

# Normalize column names (lowercase + replace spaces with underscores)
df.columns = [col.lower().replace(" ", "_") for col in df.columns]

# Display raw data info
def log_data_info(df, stage):
    print(f"\n{stage} Data Snapshot:")
    print(df.head())
    print(df.describe(include='all'))
    print(f"Missing values per column:\n{df.isnull().sum()}")

log_data_info(df, "Raw")

# Data Cleaning
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Ensure correct data types
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
df['is_fraudulent'] = df['is_fraudulent'].astype(int)  # Convert boolean to integer
df['transaction_hour'] = pd.to_numeric(df['transaction_hour'], errors='coerce').astype('Int64')
df['account_age_days'] = pd.to_numeric(df['account_age_days'], errors='coerce')
df['transaction_amount'] = pd.to_numeric(df['transaction_amount'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('Int64')

log_data_info(df, "Cleaned")

# Save cleaned data to CSV
output_file = "cleaned_Fraudulent_E-Commerce_Transaction_Data.csv"
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to {output_file}")

# Connect to PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Define schema
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    transaction_id UUID PRIMARY KEY,
    customer_id UUID,
    transaction_amount NUMERIC,
    transaction_date TIMESTAMP,
    payment_method VARCHAR(50),
    product_category VARCHAR(100),
    quantity INT,
    customer_age INT,
    customer_location VARCHAR(100),
    device_used VARCHAR(50),
    ip_address VARCHAR(50),
    shipping_address TEXT,
    billing_address TEXT,
    is_fraudulent INT,  -- Changed to INT
    account_age_days INT,
    transaction_hour INT
);
"""

# Execute schema creation
with engine.begin() as conn:
    conn.execute(text(create_table_query))

# Load data into PostgreSQL
df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
print("Data successfully loaded into PostgreSQL.")
