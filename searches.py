# Searches

# 1. Find all orders placed after a specific date
from datetime import datetime
from shop.models import *

past_month_orders = Order.objects.filter(created_at__gt=datetime.now() - datetime.timedelta(days=30))
print(f"Orders in the last 30 days: {past_month_orders.count()}")

# 2. Find all products in a specific category (assuming a 'category' field in Product)
specific_category = "Electronics"
category_products = Product.objects.filter(category=specific_category)
print(f"Products in category '{specific_category}': {category_products.count()}")

# 3. Find all customers who have placed more than a certain number of orders
min_orders = 3
frequent_customers = Order.objects.values('customer').annotate(order_count=Count('id')).filter(order_count__gt=min_orders).distinct('customer')
print(f"Customers with more than {min_orders} orders:")
for customer in frequent_customers:
    print(customer['customer'])  # Assuming 'customer' field stores customer ID

# 4. Search products by name containing a specific word (case-insensitive)
search_term = "laptop"
product_search = Product.objects.filter(name__icontains=search_term)
print(f"Products containing '{search_term}':")
for product in product_search:
    print(product)  # Print each product information
