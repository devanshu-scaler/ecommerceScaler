from rest_framework import generics, viewsets
from ..models import Product, ClothingProduct, ApplianceProduct
from ..serializers import ProductSerializer, ClothingProductSerializer, ApplianceProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # Fetch base products, excluding subclass instances
        base_products = Product.objects.exclude(
            id__in=ClothingProduct.objects.values_list('id', flat=True)
        ).exclude(
            id__in=ApplianceProduct.objects.values_list('id', flat=True)
        )

        # Fetch specific subclasses
        clothing_products = ClothingProduct.objects.all()
        appliance_products = ApplianceProduct.objects.all()

        # Combine the querysets
        combined_products = list(base_products) + list(clothing_products) + list(appliance_products)
        return combined_products