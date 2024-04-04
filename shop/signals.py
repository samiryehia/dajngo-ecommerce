from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderDetail


@receiver(post_save, sender=Order)
def decrease_product_stock(sender, instance, **kwargs):
    # Check if the order is marked as complete
    if instance.complete:
        # Get all order details for the completed order
        # I'm going to remind you guys that I have an 1:N realtionship between
        # Order and OrderDetails. 
        # I also have a 1:N realtion between Product and OrderDetails
        # The N part of the relation is the table we have the foreign key in
        order_details = OrderDetail.objects.filter(order=instance)
        
        for detail in order_details:
            # Decrease the product stock by the quantity ordered
            if detail.product and detail.quantity:
                detail.product.stock -= detail.quantity
                detail.product.save()
