DROP TABLE IF EXISTS transactions; -- <-- New line added

CREATE TABLE transactions(
	transaction_id SERIAL PRIMARY KEY,
	product_id INT,
	customer_id INT,
	quantity INT,
	price NUMERIC(10,2),
	timestamp TIMESTAMP
);

SELECT product_id, SUM(quantity*price) as total_sales
FROM transactions
GROUP BY product_id;

SELECT customer_id, SUM(quantity*price) as total_spent
FROM transactions
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 5;