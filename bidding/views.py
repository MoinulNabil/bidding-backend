from django.db.models import Sum

from rest_framework import status
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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = {}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        total_spent = PlacedBid.objects.filter(
            user=request.user,
            own=True,
        ).aggregate(total=Sum('amount'))
        total_earned = PlacedBid.objects.filter(
            product__user=request.user,
            own=True,
        ).aggregate(total=Sum('amount'))

        response['bids'] = serializer.data
        response['total_spent'] = total_spent['total'] if total_spent['total'] else 0
        response['total_earned'] = total_earned['total'] if total_earned['total'] else 0
        return Response(response)

    def get_queryset(self):
        return self.request.user.bids



class ListAllBid(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer
    

    def get_queryset(self):
        return Product.objects.order_by('-id')
        