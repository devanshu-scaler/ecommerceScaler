from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views.user_views import UserRegistrationView, UserDetailView, ShippingAddressListView, ShippingAddressDetailView, BillingAddressListView, BillingAddressDetailView
from .views.user_views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views.user_views import PasswordResetView, PasswordResetConfirmView
from .views.products_views import ProductViewSet
router = DefaultRouter()
# Register the viewset with the router
router.register(r'products', ProductViewSet, basename='product')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-registration'),
    path('login/',TokenObtainPairView.as_view(),name='user-login'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token-refresh'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('users/', UserRegistrationView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    path('users/<int:user_id>/shipping_addresses/', ShippingAddressListView.as_view(), name='shipping-address-list'),
    path('users/<int:user_id>/shipping_addresses/<int:address_pk>/', ShippingAddressDetailView.as_view(), name='shipping-address-detail'),
    
    path('users/<int:user_id>/billing_addresses/', BillingAddressListView.as_view(), name='billing-address-list'),
    path('users/<int:user_id>/billing_addresses/<int:address_pk>/', BillingAddressDetailView.as_view(), name='billing-address-detail'),
    
    path('', include(router.urls))
         
]
