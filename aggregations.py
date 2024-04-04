from shop.models import *
from django.db import connection
from django.db.models import Count, Sum, Avg, Max

# Aggregations
total_orders = Order.objects.aggregate(total=Count('id'))
# Count the total number of orders
print(f"Total Orders: {total_orders['total']}")

total_sales = OrderDetail.objects.aggregate(total_sales=Sum('total_price'))
# Calculate the total sales
print(f"Total Sales: {total_sales['total_sales']}")

avg_price = Product.objects.aggregate(avg_price=Avg('price'))
# Get the average price of products
print(f"Average Price: {avg_price['avg_price']}")

max_price = Product.objects.aggregate(max_price=Max('price'))
# Find the maximum product price
print(f"Maximum Price: {max_price['max_price']}")

total_stock = Product.objects.aggregate(total_stock=Sum('stock'))
# Calculate the total stock for all products
print(f"Total Stock: {total_stock['total_stock']}")

unique_customers = Order.objects.aggregate(unique_customers=Count('customer', distinct=True))
# Count unique customers who made an order
print(f"Unique Customers: {unique_customers['unique_customers']}")

total_products_ordered = OrderDetail.objects.aggregate(total_products=Sum('quantity'))
# Calculate the total number of products ordered
print(f"Total Products Ordered: {total_products_ordered['total_products']}")

avg_quantity_per_order = OrderDetail.objects.aggregate(avg_quantity=Avg('quantity'))
# Get the average quantity of products per order
print(f"Average Quantity per Order: {avg_quantity_per_order['avg_quantity']}")

most_expensive_product = OrderDetail.objects.order_by('-product__price').first()
# Find the most expensive product (detailed object)
print(f"Most Expensive Product: {most_expensive_product}")  # Consider filtering specific fields if needed

completed_orders = Order.objects.filter(complete=True).aggregate(total_completed=Count('id'))
# Calculate the total number of completed orders
print(f"Total Completed Orders: {completed_orders['total_completed']}")


