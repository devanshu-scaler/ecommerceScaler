from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, CreateShippingAddressSerializer, CreateBillingAddressSerializer,ShippingAddressSerializer, BillingAddressSerializer
from .models import User, ShippingAddress, BillingAddress
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


'''
Creating User Create View for registration
'''
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserRegistrationView(APIView):
    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShippingAddressListView(ListCreateAPIView):
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return ShippingAddress.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user = User.objects.get(pk=self.kwargs['user_id'])
        serializer.save(user=user)

class ShippingAddressDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer


class BillingAddressListView(ListCreateAPIView):
    serializer_class = BillingAddressSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return BillingAddress.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user = User.objects.get(pk=self.kwargs['user_id'])
        serializer.save(user=user)

class BillingAddressDetailView(RetrieveUpdateDestroyAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer


class PasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(smart_bytes(user.id))
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm') + f'?uid={uid}&token={token}'
            )
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        new_password = request.data.get('new_password')
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)