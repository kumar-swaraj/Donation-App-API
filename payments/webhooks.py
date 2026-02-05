import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payments.models import DonationPayment


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

    event_type = event['type']
    intent = event['data']['object']

    payment_intent_id = intent.get('id')

    if not payment_intent_id:
        return HttpResponse(status=200)

    if event_type == 'payment_intent.succeeded':
        DonationPayment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).exclude(status='succeeded').update(status='succeeded')

    elif event_type == 'payment_intent.payment_failed':
        DonationPayment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).exclude(status='failed').update(status='failed')

    elif event_type == 'payment_intent.processing':
        DonationPayment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).exclude(status='processing').update(status='processing')

    elif event_type == 'charge.refunded':
        DonationPayment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).exclude(status='refunded').update(status='refunded')

    return HttpResponse(status=200)
