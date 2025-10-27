import pandas as pd
import random
from faker import Faker
fake = Faker()
data = []
for i in range(100):
    data.append({
        "transaction_id": i+1,
        "product_id": random.randint(1,20),
        "customer_id": random.randint(1, 50),
        "quantity": random.randint(1,5),
        "price": round(random.uniform(50, 500), 2),
        "timestamp": fake.date_time_this_year()
        
    })

df = pd.DataFrame(data)
print(df.head())

from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:root@localhost/retail_db")
df.to_sql("transactions", engine, if_exists="append", index=False)

df["total_amount"] = df["quantity"]*df["price"]
query = "SELECT product_id, SUM(quantity*price) as total_sales FROM transactions GROUP BY product_id;"
sales_df = pd.read_sql(query, engine)
print(sales_df)

import matplotlib.pyplot as plt
plt.bar(sales_df["product_id"], sales_df["total_sales"])
plt.xlabel("Product ID")
plt.ylabel("Total Sales")
plt.title("Sales per Product")
plt.show()


