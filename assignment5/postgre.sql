CREATE TABLE weather_records (
    record_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    ingestion_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    raw_data JSONB NOT NULL
);
SELECT usename FROM pg_user;