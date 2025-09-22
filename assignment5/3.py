def insert_weather_record(conn, city, data):
    # Convert Python dictionary to JSON string
    data_json_string = json.dumps(data)
    
    sql_insert = """
    INSERT INTO weather_records (city_name, raw_data)
    VALUES (%s, %s);
    """
    
    try:
        cursor = conn.cursor()
        # Execute the INSERT statement
        cursor.execute(sql_insert, (city, data_json_string))
        conn.commit() # Save the changes to the database
        print(f"Weather data for {city} successfully inserted into PostgreSQL.")
    except Exception as e:
        conn.rollback() # Revert changes on error
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

# Execute the full process
if raw_data:
    conn = create_pg_connection()
    if conn:
        insert_weather_record(conn, CITY_NAME, raw_data)
        conn.close()