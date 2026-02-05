from django.contrib import admin, messages
from import_export.admin import ImportExportActionModelAdmin

from payments.models import DonationPayment


@admin.register(DonationPayment)
class DonationPaymentAdmin(ImportExportActionModelAdmin):
    list_display = [
        'id',
        'user',
        'donation',
        'amount',
        'currency',
        'status',
        'created_at',
    ]

    list_filter = ['status']
    search_fields = [
        'user__email',
        'user__username',
        'donation__title',
        'stripe_payment_intent_id',
    ]

    list_select_related = ['user', 'donation']
    date_hierarchy = 'created_at'
    ordering = ['-id']

    fields = [
        'id',
        'donation',
        'user',
        'amount',
        'currency',
        'stripe_payment_intent_id',
        'status',
        'created_at',
        'updated_at',
    ]

    readonly_fields = [
        'id',
        'donation',
        'user',
        'amount',
        'currency',
        'stripe_payment_intent_id',
        'created_at',
        'updated_at',
    ]

    actions = ['mark_as_refunded']

    @admin.action(description='Mark selected payments as refunded (manual)')
    def mark_as_refunded(self, request, queryset):
        updated = queryset.exclude(status='refunded').update(status='refunded')

        self.message_user(
            request,
            f'{updated} payment(s) marked as refunded.',
            level=messages.WARNING,
        )
