from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique = True)
    username = models.CharField(max_length=255, default= 'default_username',unique =True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    default_shipping_address = models.ForeignKey(
        "ShippingAddress",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_query_name="user_info"
    )
    default_billing_address = models.ForeignKey(
        "BillingAddress",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_query_name="user_info"
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        abstract = True


class ShippingAddress(Address):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipping_addresses"
    )

class BillingAddress(Address):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name ="billing_addresses"
        )