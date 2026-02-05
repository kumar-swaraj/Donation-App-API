from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q

from donations.models import Donation


class DonationPayment(models.Model):
    donation = models.ForeignKey(
        Donation,
        on_delete=models.PROTECT,
        related_name='payments',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='donation_payments',
        null=True,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=10,
        default='inr',
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
    )

    status = models.CharField(
        max_length=32,
        choices=[
            ('created', 'Created'),
            ('requires_action', 'Requires Action'),
            ('processing', 'Processing'),
            ('succeeded', 'Succeeded'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Donation payment'
        verbose_name_plural = 'Donation payments'
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gte=Decimal('0.00')),
                name='payment_amount_non_negative',
            ),
        ]

    def __str__(self):
        return f'{self.user or "Anonymous"} - {self.amount} {self.currency}'
