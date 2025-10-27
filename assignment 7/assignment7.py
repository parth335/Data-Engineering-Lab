from sqlalchemy import create_engine, text
import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine, text
fake = Faker()
engine = create_engine("postgresql+psycopg2://postgres:root@localhost/employee_db")
def create_employee(first_name, last_name, email, hire_date, role_id, dept_id):
    """Inserts a single employee record into the database."""
    sql = text("""
        INSERT INTO employees (first_name, last_name, email, hire_date, role_id, department_id)
        VALUES (:fn, :ln, :email, :hd, :rid, :did)
    """)
    try:
        with engine.connect() as connection:
            connection.execute(sql, {
                "fn": first_name, "ln": last_name, "email": email,
                "hd": hire_date, "rid": role_id, "did": dept_id
            })
            connection.commit()
            print(f"Employee {first_name} {last_name} created.")
    except Exception as e:
        print(f"Error creating employee {first_name} {last_name}: {e}")
NUM_RECORDS = 5
MAX_DEPARTMENTS = 5 
MAX_ROLES = 5        

print(f"Starting insertion of {NUM_RECORDS} synthetic employee records...")

for i in range(NUM_RECORDS):
  
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{i}@corp.com"
    hire_date = fake.date_this_decade() 
    random_role_id = random.randint(1, MAX_ROLES)
    random_dept_id = random.randint(1, MAX_DEPARTMENTS)
    
    create_employee(
        first_name, 
        last_name, 
        email, 
        hire_date, 
        random_role_id, 
        random_dept_id
    )

print("\nData insertion complete.")

def read_employees(employee_id=None):
    base_query = """
        SELECT
            e.employee_id, e.first_name, e.last_name, e.email, e.hire_date,
            r.title AS role_title, d.name AS department_name, r.salary
        FROM employees e
        JOIN roles r ON e.role_id = r.role_id
        JOIN departments d ON e.department_id = d.department_id
    """
    if employee_id:
        query = text(f"{base_query} WHERE e.employee_id = :id")
        df = pd.read_sql(query, engine, params={"id": employee_id})
    else:
        query = text(f"{base_query} ORDER BY e.employee_id")
        df = pd.read_sql(query, engine)
        
    return df
print(read_employees())

def update_employee(employee_id, new_role_id=None, new_department_id=None):
    """Modifies an existing employee's role or department."""
    updates = []
    params = {"id": employee_id}
    
    if new_role_id is not None:
        updates.append("role_id = :rid")
        params["rid"] = new_role_id
    
    if new_department_id is not None:
        updates.append("department_id = :did")
        params["did"] = new_department_id
        
    if updates:
        sql = text(f"UPDATE employees SET {', '.join(updates)} WHERE employee_id = :id")
        with engine.connect() as connection:
            result = connection.execute(sql, params)
            connection.commit()
            print(f" Updated {result.rowcount} row(s) for Employee ID {employee_id}.")
    else:
        print("No fields provided for update.")
print("\n--- UPDATE: Employee 1 ---")
update_employee(employee_id=156, new_role_id=3, new_department_id=1)
print(read_employees(employee_id=1))

def delete_employee(employee_id):
    """Permanently removes an employee record."""
    sql = text("DELETE FROM employees WHERE employee_id = :id")
    with engine.connect() as connection:
        result = connection.execute(sql, {"id": employee_id})
        connection.commit()
        print(f" Deleted {result.rowcount} row(s). Employee ID {employee_id} removed.")
print("\n--- DELETE: Employee 157 ---")
delete_employee(employee_id=157)

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
analysis_query = text("""
    SELECT r.title, AVG(r.salary) AS avg_salary, COUNT(e.employee_id) AS total_employees
    FROM employees e
    JOIN roles r ON e.role_id = r.role_id
    GROUP BY r.title
    ORDER BY avg_salary DESC
""")

average_salaries_df = pd.read_sql(analysis_query, engine)
print("\nAverage Salary per Role:")
print(average_salaries_df)

average_salaries_df = average_salaries_df.sort_values(by='avg_salary', ascending=True)
plt.figure(figsize=(10, 6))
plt.barh(
    average_salaries_df['title'],
    average_salaries_df['avg_salary'],
    color='skyblue'
)
plt.title("Average Employee Salary by Role")
plt.xlabel("Average Salary (USD)")
plt.ylabel("Role Title")
plt.ticklabel_format(style='plain', axis='x')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()