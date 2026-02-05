from rest_framework import serializers

from payments.models import DonationPayment


class MyDonationSerializer(serializers.ModelSerializer):
    donation_title = serializers.CharField(source='donation.title', read_only=True)

    class Meta:
        model = DonationPayment
        fields = [
            'id',
            'donation_title',
            'amount',
            'currency',
            'status',
            'created_at',
        ]
