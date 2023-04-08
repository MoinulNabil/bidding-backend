from rest_framework import status
from rest_framework import parsers
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Product,
    PlacedBid
)
from .serializers import (
    ProductSerializer,
    PlaceBidSerializer,
    UserBidSerializer,
    ProductDetailsSerializer
)
from user_account.permissions import (
    IsProductCreator
)


class ListCreateProduct(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.products
    

class RetrieveUpdateDestroyProduct(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProductCreator, ]
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()


class RetrieveProduct(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductDetailsSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()


class PlaceBid(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PlaceBidSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ListUserBid(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserBidSerializer

    def get_queryset(self):
        return self.request.user.bids



class ListAllBid(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        context = {}
        