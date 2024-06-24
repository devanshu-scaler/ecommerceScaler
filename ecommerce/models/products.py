import uuid
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=255, default='images/products/')
    price_cents = models.IntegerField()  # Cent amount for price
    keywords = models.JSONField(default=list)
    stars = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        db_table ='products'
    
    def get_stars(self):
        # Dummy method to simulate the stars rating; you should replace this with actual logic
        return 4.5

    def get_rating_count(self):
        # Dummy method to simulate rating count; replace with actual logic
        return 87
    
class ClothingProduct(Product):
    type = models.CharField(max_length=100, default='clothing')
    
    class Meta:
        db_table = 'clothingproducts'
    
class ApplianceProduct(Product):
    type = models.CharField(max_length=100, default='appliance')
    warranty_link = models.CharField(max_length=255, default = 'images/products/appliance-warranty.png');
    instruction_link = models.CharField(max_length=255, default='images/products/appliance-instructions.png');
    
    class Meta:
        db_table = 'applianceproducts'