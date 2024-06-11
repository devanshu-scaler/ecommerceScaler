from rest_framework import serializers
from .models import User, ShippingAddress, BillingAddress

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    default_shipping_address = ShippingAddressSerializer(read_only=True)
    default_billing_address = BillingAddressSerializer(read_only=True)
    shipping_addresses = ShippingAddressSerializer(many = True, read_only = True)
    billing_addresses = BillingAddressSerializer(many = True, read_only = True)
    class Meta:
        model = User
        fields = ('email', 'user', 'password', 'created_at', 'updated_at', 'default_shipping_address','shipping_addresses', 'default_billing_address','billing_addresses')

    def create(self, validated_data):
        # Hash the password before creating the user
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

class CreateShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('street', 'city', 'state', 'zip_code', 'country')

class CreateBillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ('street', 'city', 'state', 'zip_code', 'country')
