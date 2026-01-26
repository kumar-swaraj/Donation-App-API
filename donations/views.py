from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Donation
from .serializers import CategoryWithDonationSerializer, DonationSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories(request):
    categories = Category.objects.prefetch_related('donations').order_by('id')
    serializer = CategoryWithDonationSerializer(
        categories, many=True, context={'request': request}
    )
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def donation(request, pk):
    donation = get_object_or_404(
        Donation.objects.prefetch_related('categories').order_by('id'), id=pk
    )

    serializer = DonationSerializer(donation, many=False, context={'request': request})
    return Response(serializer.data, status.HTTP_200_OK)
