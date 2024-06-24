from rest_framework import serializers
from ..models import User, ShippingAddress, BillingAddress
from django.contrib.auth.hashers import make_password

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
        fields = ('id','email', 'username', 'password', 'created_at','is_active',
         'updated_at', 'default_shipping_address',
         'shipping_addresses', 'default_billing_address','billing_addresses')

    def create(self, validated_data):
        # Hash the password before creating the user
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        # validated_data['password'] = make_password(validated_data['password'])
        

        print(instance);

        # Update default shipping address
        if 'default_shipping_address' in self.initial_data:
            shipping_data = self.initial_data.pop('default_shipping_address')
            if shipping_data:
                if instance.default_shipping_address:
                    for attr, value in shipping_data.items():
                        setattr(instance.default_shipping_address, attr, value)
                    instance.default_shipping_address.save()
                else:
                    shipping_address = ShippingAddress.objects.create(user=instance, **shipping_data)
                    instance.default_shipping_address = shipping_address

        # Update default billing address
        if 'default_billing_address' in self.initial_data:
            billing_data = self.initial_data.pop('default_billing_address')
            if billing_data:
                if instance.default_billing_address:
                    for attr, value in billing_data.items():
                        setattr(instance.default_billing_address, attr, value)
                    instance.default_billing_address.save()
                else:
                    billing_address = BillingAddress.objects.create(user=instance, **billing_data)
                    instance.default_billing_address = billing_address

        # Handling updates to the shipping and billing addresses separately
        if 'shipping_addresses' in self.initial_data:
            shipping_addresses_data = self.initial_data.get('shipping_addresses')
            for address_data in shipping_addresses_data:
                ShippingAddress.objects.update_or_create(id=address_data.get('id'), user=instance, defaults=address_data)

        if 'billing_addresses' in self.initial_data:
            billing_addresses_data = self.initial_data.get('billing_addresses')
            for address_data in billing_addresses_data:
                BillingAddress.objects.update_or_create(id=address_data.get('id'), user=instance, defaults=address_data)

        instance.save()
        return instance

class CreateShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('street', 'city', 'state', 'zip_code', 'country')

class CreateBillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ('street', 'city', 'state', 'zip_code', 'country')
