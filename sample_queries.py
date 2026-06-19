"""Sample SQL queries for testing the formatter"""

SAMPLE_QUERIES = {
    "Simple SELECT": """
select id,name,email from users where status='active' and created_at>='2024-01-01'
""",
    
    "Multiple Joins": """
SELECT o.order_id,o.order_date,c.customer_name,p.product_name,oi.quantity,oi.price FROM orders o JOIN customers c ON o.customer_id=c.customer_id JOIN order_items oi ON o.order_id=oi.order_id JOIN products p ON oi.product_id=p.product_id WHERE o.order_date BETWEEN '2024-01-01' AND '2024-12-31' AND o.status='completed'
""",
    
    "Complex with CTEs": """
WITH monthly_sales AS (SELECT DATE_TRUNC('month',order_date) as month,SUM(total_amount) as revenue FROM orders GROUP BY 1),top_customers AS (SELECT customer_id,SUM(total_amount) as lifetime_value FROM orders GROUP BY customer_id HAVING SUM(total_amount)>10000) SELECT ms.month,ms.revenue,COUNT(DISTINCT tc.customer_id) as vip_customers FROM monthly_sales ms LEFT JOIN orders o ON DATE_TRUNC('month',o.order_date)=ms.month LEFT JOIN top_customers tc ON o.customer_id=tc.customer_id GROUP BY ms.month,ms.revenue ORDER BY ms.month DESC
""",
    
    "Nested Subqueries": """
SELECT customer_id,customer_name,(SELECT COUNT(*) FROM orders WHERE customer_id=c.customer_id) as order_count,(SELECT AVG(total_amount) FROM orders WHERE customer_id=c.customer_id) as avg_order_value FROM customers c WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders WHERE order_date>='2024-01-01')
"""
}
