import pandas as pd
from sqlalchemy import create_engine

# Use raw strings or forward slashes here
basic_info_table = pd.read_excel("D:/AI_Video/jr ds files/basic_info.xlsx")
delivery_info_table = pd.read_excel("D:/AI_Video/jr ds files/delivery_info.xlsx")
followup_data_table = pd.read_excel("D:/AI_Video/jr ds files/followup_data.xlsx")

# PostgreSQL connection details
db_name = "healthcare_db"
user = "neondb_owner"
password = "npg_fT7BkJdyptG0"
host = "ep-proud-wildflower-a8k5dh09-pooler.eastus2.azure.neon.tech"
port = "5432"

# Create engine
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')

# Upload tables
basic_info_table.to_sql('basic_info', engine, schema='public', if_exists='append', index=False)
delivery_info_table.to_sql('delivery_info_field', engine, schema='public', if_exists='append', index=False)
followup_data_table.to_sql('followup_data', engine, schema='public', if_exists='append', index=False)

print("All data inserted successfully.")
