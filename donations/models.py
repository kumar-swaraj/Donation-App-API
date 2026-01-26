from decimal import Decimal

from django.db import models
from django.db.models import Q


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=48, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Donation(TimeStampedModel):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='donations')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00')
    )
    image = models.ImageField(upload_to='donations', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gte=0),
                name='amount_non_negative',
            )
        ]

    def __str__(self):
        return self.title
