from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, CreateShippingAddressSerializer, CreateBillingAddressSerializer,ShippingAddressSerializer, BillingAddressSerializer
from .models import User, ShippingAddress, BillingAddress


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
