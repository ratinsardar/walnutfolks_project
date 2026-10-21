from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    source_account = models.CharField(max_length=255)
    destination_account = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

