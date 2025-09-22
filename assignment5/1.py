import psycopg2

def create_pg_connection():
    try:
        conn = psycopg2.connect(
            database="weather2_db",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None