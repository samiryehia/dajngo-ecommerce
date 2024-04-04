from shop.models import *
from django.db import connection
from django.db.models import Count, Sum, Avg, Max


products = Product.objects.all()

# Model.objects.method()
# Table.manager.QuerySetOperation()
for product in products:
    print(product.name + ":" + str(product.price))

filter_products = Product.objects.filter(price=500) 

for product in filter_products:
    print("The following product is priced at $500 " + product.name) 

#Lookups
#__gt 
#__gte
# __lt
#__lte
filter_products_price= Product.objects.filter(price__gt=50)

for product in filter_products_price:
    print("The list of product(s) is priced greater than 50$:\n" + product.name)

#get method returns one product (object) ONLY.
# I would get a MultipleObjectsReturned Error/DoesNotExistError if multiple or no objects are returned

specific_product = Product.objects.get(pk=2)

print("Product with primary key (pk) = 2: " + str(specific_product))

entry_exists = Product.objects.filter(pk=2).exists()

print(entry_exists)

Product.objects.create()



# Aggregations
total_orders = Order.objects.aggregate(total=Count('id'))

total_sales = OrderDetail.objects.aggregate(total_sales=Sum('total_price'))

avg_price = Product.objects.aggregate(avg_price=Avg('price'))

max_price = Product.objects.aggregate(max_price=Max('price'))

total_stock = Product.objects.aggregate(total_stock=Sum('stock'))

unique_customers = Order.objects.aggregate(unique_customers=Count('customer', distinct=True))

total_products_ordered = OrderDetail.objects.aggregate(total_products=Sum('quantity'))

avg_quantity_per_order = OrderDetail.objects.aggregate(avg_quantity=Avg('quantity'))

most_expensive_product = OrderDetail.objects.order_by('-product__price').first()

completed_orders = Order.objects.filter(complete=True).aggregate(total_completed=Count('id'))



# Searches
laptops = Product.objects.filter(name__icontains='laptop')
customer_orders = Order.objects.filter(customer__email='example@example.com')
