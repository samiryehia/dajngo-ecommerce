# Importing necessary classes from Django's database (db) module.
from django.db import models 
from django.db.models import *
# This import is redundant as we are not using any specific models function explicitly besides 'models' already imported.
from django.db.models import *
# Importing the User model from Django's built-in authentication system.
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.timezone import now



# Definition of the Customer model that extends models.Model.
class Customer(models.Model):
    #In the database, this would be named by default: shop_customer

    # Creates a one-to-one relationship between the Customer and User models.
    # This means each Customer is linked to a single User, and vice versa.
    # on_delete=models.CASCADE means if the linked User is deleted, the Customer will be deleted too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # CharField is used for storing character or string data, max_length defines the maximum number of characters.
    name = models.CharField(max_length=200)
    # EmailField is a specialized CharField for storing email addresses.
    email = models.EmailField()

    # This method returns the customer's name when its instance is called in a string context.
    def __str__(self):
        return self.name
    
    # Meta options for the Customer model.
    class Meta:
        # Defines the name of the database table to be used for the Customer model.
        db_table = 'customer_info'
        # Verbose name for a single instance of the model.
        verbose_name = 'Customer'
        # Verbose name for multiple instances of the model.
        verbose_name_plural = 'Customers'

# Definition of the Product model that extends models.Model.
class Product(models.Model):
    # Fields definition similar to Customer, with additional fields for product details.
    name = models.CharField(max_length=200)
    # DecimalField is used for storing decimal numbers, with max_digits and decimal_places.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    # ImageField for storing image files, with upload_to specifying the directory where files will be stored.
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    # Similar __str__ method as Customer, returns the product name.
    def __str__(self):
        return self.name
    
    # Meta class with ordering and verbose names defined.
    class Meta:
        # Orders instances of the model by price in descending order.
        ordering = ['-price']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

# Definition of the Order model.
class Order(models.Model):
    # ForeignKey creates a many-to-one relationship. Here, many orders can be associated with one customer.
    # SET_NULL on deletion of the referenced object means the foreign key becomes NULL instead of deleting the instance.
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    # DateTimeField with auto_now_add=True automatically sets the field to the current date and time when the object is created.
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    # Method to calculate the total price of the order.
    def get_total_price(self):
        # Logic to calculate total; placeholder as it refers to non-existent fields 'product' and 'quantity'.
        if self.product and self.quantity:
            return self.product.price * self.quantity
        else:
            return 0
    
    # Returns the order ID as a string representation of the object.
    def __str__(self):
        return str(self.id)



# Definition of the OrderDetail model.
class OrderDetail(models.Model):
    # Defines a many-to-one relationship to both Product and Order.
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # Automatically sets the field to the current date and time when the object is created.
    date_added = models.DateTimeField(auto_now_add=True)

    # Method overridden to provide custom save functionality.
    def save(self, *args, **kwargs):
        # Calculates total price before saving, based on product price and quantity.
        if self.product and self.quantity:
            self.total_price = self.product.price * self.quantity
        else:
            self.total_price = 0
        # Calls the parent class's save method to handle the actual saving.
        super().save(*args, **kwargs)
    
    # Returns the product's string representation.
    def __str__(self):
        return str(self.product)
    
    # Decimal field to store the calculated total price.
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Meta class for additional options.
    class Meta:
        # Ensures that each combination of product and order is unique.
        unique_together = (('product', 'order'),)
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

class LoggingRecord(models.Model):
    """
    Model to store logging records.
    """
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255, null=True)
    status_code = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user} - {self.method} {self.path} - {self.status_code}"