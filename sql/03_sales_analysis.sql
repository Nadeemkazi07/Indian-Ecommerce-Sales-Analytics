CREATE DATABASE ecommerce_analytics;

USE ecommerce_analytics;
SELECT COUNT(*) AS total_orders
FROM sales;
SELECT 
    ROUND(SUM(Sales_INR), 2) AS total_revenue
FROM sales;
SELECT 
    ROUND(SUM(Profit_INR), 2) AS total_profit
FROM sales;
SELECT 
    SUM(Quantity) AS total_units_sold
FROM sales;
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT Customer_ID) AS total_customers,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit,
    ROUND(
        SUM(Profit_INR) / SUM(Sales_INR) * 100,
        2
    ) AS profit_margin_pct
FROM sales;
SELECT
    Order_Month,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit,
    COUNT(*) AS orders
FROM sales
GROUP BY Order_Month
ORDER BY Order_Month;
SELECT
    State,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit,
    COUNT(*) AS orders
FROM sales
GROUP BY State
ORDER BY revenue DESC;
SELECT
    City,
    State,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit,
    COUNT(*) AS orders
FROM sales
GROUP BY City, State
ORDER BY revenue DESC
LIMIT 10;
SELECT
    Category,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit,
    SUM(Quantity) AS units_sold,
    ROUND(
        SUM(Profit_INR) / SUM(Sales_INR) * 100,
        2
    ) AS profit_margin_pct
FROM sales
GROUP BY Category
ORDER BY revenue DESC;
SELECT
    Product,
    Category,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit
FROM sales
GROUP BY Product, Category
ORDER BY revenue DESC
LIMIT 10;
SELECT
    Product,
    Category,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit
FROM sales
GROUP BY Product, Category
ORDER BY profit DESC
LIMIT 10;
SELECT
    Customer_ID,
    Customer_Type,
    COUNT(*) AS orders,
    SUM(Quantity) AS units_purchased,
    ROUND(SUM(Sales_INR), 2) AS total_spend,
    ROUND(SUM(Profit_INR), 2) AS total_profit
FROM sales
GROUP BY Customer_ID, Customer_Type
ORDER BY total_spend DESC
LIMIT 10;
SELECT
    Customer_Type,
    COUNT(DISTINCT Customer_ID) AS customers,
    COUNT(*) AS orders,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit
FROM sales
GROUP BY Customer_Type;
SELECT
    Payment_Method,
    COUNT(*) AS orders,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(AVG(Sales_INR), 2) AS average_order_value
FROM sales
GROUP BY Payment_Method
ORDER BY revenue DESC;
SELECT
    Returned,
    COUNT(*) AS orders
FROM sales
GROUP BY Returned;
SELECT
    ROUND(
        SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS return_rate_pct
FROM sales;
SELECT
    Return_Reason,
    COUNT(*) AS return_count
FROM sales
WHERE Returned = 'Yes'
GROUP BY Return_Reason
ORDER BY return_count DESC;
SELECT
    Discount_Pct,
    COUNT(*) AS orders,
    ROUND(SUM(Sales_INR), 2) AS revenue,
    ROUND(SUM(Profit_INR), 2) AS profit,
    ROUND(
        SUM(Profit_INR) / SUM(Sales_INR) * 100,
        2
    ) AS profit_margin_pct
FROM sales
GROUP BY Discount_Pct
ORDER BY Discount_Pct;
SELECT
    Delivery_Days,
    COUNT(*) AS orders,
    ROUND(AVG(Customer_Rating), 2) AS avg_rating
FROM sales
GROUP BY Delivery_Days
ORDER BY Delivery_Days;