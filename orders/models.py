from django.db import models
from django.conf import settings
from product.models import Product



class Order(models.Model):

    class Status(models.TextChoices):
        PENDING_PAYMENT = 'PENDING_PAYMENT', 'Pending Payment'
        PAID = 'PAID', 'Paid'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    status= models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    total_price= models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} - {self.customer.email} - {self.status}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at'] 
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_price__gte=0),
                name='total_price_non_negative'
            ),
        ]


class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity= models.PositiveIntegerField()
    unit_price= models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} (x{self.quantity}) - Order {self.order.id}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name='quantity_positive'
            ),
            models.CheckConstraint(
                check=models.Q(unit_price__gte=0),
                name='price_non_negative'
            ),
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_product'
            )
        ]