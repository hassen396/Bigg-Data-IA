# The insight generated on Power bi is located here https://drive.google.com/drive/folders/1STB9QD5s7hLbEBrx1H59BhuiWx3YivEC?usp=sharing  (I was unable to upload the data because of the size limit imposed by Github)

# E-Commerce Fraud Detection Data Processing

## Overview
This project focuses on processing a dataset containing e-commerce transactions, cleaning the data, and loading it into a PostgreSQL database for further analysis. The dataset includes details such as transaction amounts, customer locations, payment methods, and fraud indicators. The goal is to ensure data integrity, prepare the data for analysis, and store it in a structured database.

---

## Requirements
To run this project, you need the following:

### Python Libraries
- **Pandas**: For data manipulation and analysis.
- **SQLAlchemy**: For connecting to and interacting with the PostgreSQL database.
- **psycopg2**: For PostgreSQL database adapter.
- **kagglehub**: For downloading the dataset from Kaggle.

### Software
- **Python 3.x**: The programming language used for the project.
- **PostgreSQL**: The database system used to store the processed data.

---

## Dataset
The dataset used in this project is **Fraudulent_E-Commerce_Transaction_Data.csv**, which contains 16 columns of e-commerce transaction data. The dataset includes the following fields:

| Column Name          | Description                          | Data Type   |
|----------------------|--------------------------------------|-------------|
| transaction_id       | Unique identifier for each transaction | UUID        |
| customer_id          | Unique identifier for each customer   | UUID        |
| transaction_amount   | Amount spent in the transaction      | NUMERIC     |
| transaction_date     | Date and time of the transaction     | TIMESTAMP   |
| payment_method       | Method used for payment              | VARCHAR(50) |
| product_category     | Category of the purchased product    | VARCHAR(100)|
| quantity             | Number of items in the transaction   | INT         |
| customer_age         | Age of the customer                  | INT         |
| customer_location    | Geographical location of the customer| VARCHAR(100)|
| device_used          | Device type used for the transaction | VARCHAR(50) |
| ip_address           | IP address used during the transaction| VARCHAR(50) |
| shipping_address     | Address to which the order was shipped| TEXT        |
| billing_address      | Billing address of the customer      | TEXT        |
| is_fraudulent        | Indicator of fraudulent transactions | INT         |
| account_age_days     | Age of the customer account in days  | INT         |
| transaction_hour     | Hour of the day the transaction occurred | INT     |

---

## Project Structure
The project consists of two main scripts:

1. **Download Dataset Script**:
   - Downloads the dataset from Kaggle using the `kagglehub` library.
   - Saves the dataset to the `original_data` folder.

2. **Data Processing Script**:
   - Loads the dataset into a Pandas DataFrame.
   - Cleans the data by removing duplicates, handling missing values, and ensuring correct data types.
   - Saves the cleaned data to a new CSV file.
   - Connects to a PostgreSQL database and creates a table to store the cleaned data.
   - Loads the cleaned data into the PostgreSQL database.

---

## How to Run the Project

### Step 1: Set Up the Environment
1. Install the required Python libraries:
   ```bash
   pip install pandas sqlalchemy psycopg2 kagglehub
   ```
   Set up a PostgreSQL database:

Create a database named ecommerce_db.

Update the database connection details in the script if necessary:

```python
DB_USER = "smilex"
DB_PASSWORD = "smilex"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ecommerce_db"
```
### Step 2: Download the Dataset
Run the following script to download the dataset from Kaggle and save it to the original_data folder:
```python
import kagglehub
import shutil
import os

# Define target directory
target_dir = "original_data"

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# Download the dataset
path = kagglehub.dataset_download("shriyashjagtap/fraudulent-e-commerce-transactions")

# Move the downloaded dataset to data/raw
for file in os.listdir(path):
    shutil.move(os.path.join(path, file), os.path.join(target_dir, file))

print(f"Dataset saved to: {target_dir}")
```
### Step 3: Process the Data
Run the following script to clean the data and load it into the PostgreSQL database:
```python
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
```
### Output
    Cleaned Data:

### The cleaned dataset is saved as cleaned_Fraudulent_E-Commerce_Transaction_Data.csv.

    Postgr eSQL Database:

### The cleaned data is loaded into the transactions table in the ecommerce_db PostgreSQL database.
### Insights from the Data
    The processed data can be used for further analysis, such as:

    Analyzing the distribution of fraudulent transactions.

    Exploring customer demographics and behavior.

### Conclusion
    This project demonstrates the process of downloading, cleaning, and storing e-commerce transaction data in a PostgreSQL database. The cleaned data is ready for further analysis and visualization to gain insights into transaction patterns and fraud detection.
### Submission Date
    February 2025

