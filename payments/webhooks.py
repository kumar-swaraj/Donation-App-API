import logging

import stripe
from django.conf import settings
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payments.models import DonationPayment, StripeEvent

logger = logging.getLogger(__name__)


def _extract_payment_intent_id(obj):
    """Extract payment_intent_id from Stripe event object."""
    if obj.get('object') == 'payment_intent':
        return obj.get('id')
    elif obj.get('object') == 'charge':
        return obj.get('payment_intent')
    return None


def _update_donation_payment_status(payment_intent_id, event_type):
    """Update DonationPayment status based on event type."""
    qs = DonationPayment.objects.filter(stripe_payment_intent_id=payment_intent_id)

    if event_type == 'payment_intent.succeeded':
        qs.exclude(status='succeeded').update(status='succeeded')
    elif event_type == 'payment_intent.payment_failed':
        qs.exclude(status='failed').update(status='failed')
    elif event_type == 'payment_intent.processing':
        qs.exclude(status='processing').update(status='processing')
    elif event_type == 'charge.refunded':
        qs.exclude(status='refunded').update(status='refunded')
    else:
        return False
    return True


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_id = event['id']
    event_type = event['type']
    obj = event['data']['object']

    # Resolve PaymentIntent ID safely
    payment_intent_id = _extract_payment_intent_id(obj)

    # -------------------------
    # Idempotency guard
    # -------------------------
    try:
        with transaction.atomic():
            StripeEvent.objects.create(
                event_id=event_id,
                event_type=event_type,
                payment_intent_id=payment_intent_id,
            )
    except IntegrityError:
        # Event already processed → idempotent success
        return HttpResponse(status=200)

    # -------------------------
    # Apply state transition
    # -------------------------
    if not payment_intent_id:
        logger.warning(
            'Stripe event without payment_intent',
            extra={'event_id': event_id, 'event_type': event_type},
        )
        return HttpResponse(status=200)

    with transaction.atomic():
        if not _update_donation_payment_status(payment_intent_id, event_type):
            logger.info(
                'Unhandled Stripe event',
                extra={'event_id': event_id, 'event_type': event_type},
            )

    return HttpResponse(status=200)
