from rest_framework import serializers
from ..models import Product, ClothingProduct, ApplianceProduct

class RatingSerializer(serializers.Serializer):
    stars = serializers.FloatField()
    count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex')
    image = serializers.CharField()
    priceCents = serializers.IntegerField(source='price_cents')
    keywords = serializers.ListField(child=serializers.CharField())
    rating = RatingSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'priceCents', 'keywords', 'rating']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add rating field dynamically
        representation['rating'] = {
            "stars": instance.stars,
            "count": instance.rating_count
        }
        
        # Handle type-specific fields
        if isinstance(instance, ClothingProduct):
            print('clothing entered')
            representation['type'] = 'clothing'
            representation['sizeChartLink'] = 'images/clothing-size-chart.png'
        elif isinstance(instance, ApplianceProduct):
            print('appliance entered')
            representation['type'] = 'appliance'
            representation['warrantyLink'] = instance.warranty_link
            representation['instructionLink'] = instance.instruction_link
        return representation
    
class ClothingProductSerializer(ProductSerializer):
    sizeChartLink = serializers.CharField(default='images/clothing-size-chart.png')

    class Meta:
        model = ClothingProduct
        fields = ProductSerializer.Meta.fields + ['type', 'sizeChartLink']

class ApplianceProductSerializer(ProductSerializer):
    warrantyLink = serializers.CharField(source='warranty_link')
    instructionLink = serializers.CharField(source='instruction_link')

    class Meta:
        model = ApplianceProduct
        fields = ProductSerializer.Meta.fields + ['type', 'warrantyLink', 'instructionLink']
