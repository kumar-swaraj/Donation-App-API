from django.contrib import admin, messages
from import_export.admin import ExportMixin, ImportExportActionModelAdmin

from payments.models import DonationPayment, StripeEvent
from payments.resources import StripeEventResource


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


@admin.register(StripeEvent)
class StripeEventAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StripeEventResource

    list_display = [
        'event_id',
        'event_type',
        'payment_intent_id',
        'processed_at',
    ]

    list_filter = ['event_type']
    search_fields = ['event_id', 'payment_intent_id']
    ordering = ['-processed_at']
    date_hierarchy = 'processed_at'

    readonly_fields = [
        'event_id',
        'event_type',
        'payment_intent_id',
        'processed_at',
    ]

    fields = readonly_fields

    # ---- hard locks ----
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
