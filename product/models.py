from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock= models.PositiveIntegerField(default=0)
    reserved_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def available_stock(self):
        return self.stock - self.reserved_stock

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(stock__gte=0),
                name='stock_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(reserved_stock__gte=0),
                name='reserved_stock_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(reserved_stock__lte=models.F('stock')),
                name='reserved_stock_lte_stock'
            ),
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name='price_non_negative'
            ),
        ]

    