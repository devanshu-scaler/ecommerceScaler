from django.contrib import admin
from .models import Product
from django.contrib import admin
from .models import User, ShippingAddress, BillingAddress
from .models import Product, ApplianceProduct, ClothingProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_price', 'get_stars', 'get_rating_count')
    list_filter = ('keywords',)

    def get_price(self, obj):
        return obj.price_cents / 100  # Convert cents to dollars
    get_price.short_description = 'Price ($)'

    def get_stars(self, obj):
        return obj.stars
    get_stars.short_description = 'Stars'

    def get_rating_count(self, obj):
        return obj.rating_count
    get_rating_count.short_description = 'Rating Count'
    # Additional customization if necessary

admin.site.register(Product, ProductAdmin)
admin.site.register(ClothingProduct, ProductAdmin)
admin.site.register(ApplianceProduct, ProductAdmin)


# Register your models here.
from django.contrib import admin
from .models import User, ShippingAddress, BillingAddress
from .models import Product, ApplianceProduct, ClothingProduct


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'default_shipping_address', 'default_billing_address')
    list_filter = ('is_active',)
    search_fields = ('email', 'username')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'zip_code', 'country')
    search_fields = ('user__email', 'street', 'city')

class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'zip_code', 'country')
    search_fields = ('user__email', 'street', 'city')

admin.site.register(User, UserAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
