from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Category, Donation


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']


class DonationWithoutCategorySerializer(ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = [
            'id',
            'title',
            'description',
            'amount',
            'image',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if not obj.image:
            return None
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class CategoryWithDonationSerializer(CategorySerializer):
    donations = DonationWithoutCategorySerializer(many=True, read_only=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['donations']


class DonationSerializer(DonationWithoutCategorySerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta(DonationWithoutCategorySerializer.Meta):
        fields = DonationWithoutCategorySerializer.Meta.fields + ['categories']
