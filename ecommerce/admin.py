# Register your models here.
from django.contrib import admin
from .models import User, ShippingAddress, BillingAddress

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
