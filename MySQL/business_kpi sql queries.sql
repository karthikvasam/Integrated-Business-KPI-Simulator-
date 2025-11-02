use business_kpi;

---------------

create user if not exists 'powerbiuser' identified by 'karthik@3480';
grant select on business_kpi.* to 'powerbiuser';
flush privileges;

---------------------

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sku VARCHAR(64) UNIQUE,
  name VARCHAR(255),
  category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS stores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200),
  city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS sales (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  store_id INT NOT NULL,
  sale_date DATE NOT NULL,
  qty INT NOT NULL,
  price_per_unit DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (store_id) REFERENCES stores(id)
);

-------------------------------------

INSERT INTO products (sku, name, category) VALUES
('SKU-001','Idli Rice','Food'),
('SKU-002','Dosa Rice','Food'),
('SKU-003','Sambar Powder','Food');

INSERT INTO stores (name, city) VALUES
('Geetha Bhavan Main', 'Manchiryal'),
('Geetha Bhavan Branch', 'Hyderabad');

INSERT INTO sales (product_id, store_id, sale_date, qty, price_per_unit) VALUES
(1, 1, '2025-10-01', 50, 30.00),
(2, 1, '2025-10-01', 30, 35.00),
(1, 2, '2025-10-02', 70, 29.50),
(3, 2, '2025-10-03', 20, 120.00),
(2, 1, '2025-10-04', 15, 35.00);

--------------------------------------------

CREATE OR REPLACE VIEW v_total_revenue AS
SELECT SUM(qty * price_per_unit) AS total_revenue
FROM sales;

CREATE OR REPLACE VIEW v_revenue_by_product AS
SELECT p.id AS product_id,
       p.name AS product,
       p.category,
       SUM(s.qty * s.price_per_unit) AS revenue,
       SUM(s.qty) AS units_sold
FROM sales s
JOIN products p ON p.id = s.product_id
GROUP BY p.id, p.name, p.category;

CREATE OR REPLACE VIEW v_revenue_by_store AS
SELECT st.id AS store_id,
       st.name AS store,
       st.city,
       SUM(s.qty * s.price_per_unit) AS revenue,
       SUM(s.qty) AS units_sold
FROM sales s
JOIN stores st ON st.id = s.store_id
GROUP BY st.id, st.name, st.city;

CREATE OR REPLACE VIEW v_daily_sales AS
SELECT sale_date,
       SUM(qty) AS units_sold,
       SUM(qty * price_per_unit) AS revenue
FROM sales
GROUP BY sale_date
ORDER BY sale_date;

----------------------------------------------------------

SET SESSION cte_max_recursion_depth = 2000;  -- increase if needed

TRUNCATE TABLE dim_date;

INSERT IGNORE INTO dim_date (date_id, year, month, day, day_of_week, month_name, quarter)
WITH RECURSIVE seq AS (
  SELECT CAST('2024-01-01' AS DATE) AS dt
  UNION ALL
  SELECT DATE_ADD(dt, INTERVAL 1 DAY) FROM seq WHERE dt < '2025-12-31'
)
SELECT dt,
       YEAR(dt),
       MONTH(dt),
       DAY(dt),
       DAYOFWEEK(dt),
       DATE_FORMAT(dt, '%M'),
       QUARTER(dt)
FROM seq;

SELECT * FROM fact_sales LIMIT 10;

SELECT fs.sale_id, fs.product_id, fs.sale_date, dd.month_name, dd.quarter
FROM fact_sales fs
JOIN dim_date dd ON fs.sale_date = dd.date_id
LIMIT 10;


