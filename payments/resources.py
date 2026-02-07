from import_export import resources

from payments.models import StripeEvent


class StripeEventResource(resources.ModelResource):
    class Meta:
        model = StripeEvent
        fields = (
            'event_id',
            'event_type',
            'payment_intent_id',
            'processed_at',
        )
        export_order = fields
