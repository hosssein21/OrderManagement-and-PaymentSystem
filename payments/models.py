from django.db import models

class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESSFUL = 'SUCCESSFUL', 'Successful'
        UNKNOWN = 'UNKNOWN', 'Unknown'
        FAILED = 'FAILED', 'Failed'

    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='payments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=50)
    provider_reference = models.CharField(max_length=100, blank=True, null=True)
    idempotency_key = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Payment for Order {self.order.id} - Status: {self.status}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name='amount_positive'
            ),
            models.UniqueConstraint(
                fields=['provider', 'provider_reference'],
                name='unique_provider_reference'
            )
        ]