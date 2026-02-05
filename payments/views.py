from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from donations.models import Donation
from payments.models import DonationPayment
from payments.serializers import MyDonationSerializer
from payments.stripe_client import stripe


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stripe_publishable_key(request):
    return Response(
        {'stripePublishableKey': settings.STRIPE_PUBLISHABLE_KEY},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    donation_id = request.data.get('donation_id')
    if not donation_id:
        return Response(
            {'error': 'donation_id is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    donation = get_object_or_404(Donation, id=donation_id, is_active=True)

    with transaction.atomic():
        payment = DonationPayment.objects.create(
            donation=donation,
            user=request.user,
            amount=donation.amount,
            currency='inr',
            status='created',
            stripe_payment_intent_id='pending',
        )

        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),
            currency=payment.currency,
            metadata={
                'payment_id': payment.id,
                'donation_id': donation_id,
                'user_id': request.user.id,
            },
            automatic_payment_methods={'enabled': True},
        )

        payment.stripe_payment_intent_id = intent.id
        payment.save(update_fields=['stripe_payment_intent_id'])

    return Response(
        {'clientSecret': intent.client_secret},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_donations(request):
    donation_payments = (
        DonationPayment.objects.filter(user=request.user)
        .select_related('donation')
        .order_by('-created_at')
    )

    serializer = MyDonationSerializer(donation_payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
