from django.db.models import Sum
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from bidding.models import PlacedBid

from .serializers import (
    UserSerializer
)


User = get_user_model()


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class Analytics(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get(self, *args, **kwargs):
        response = {}
        total_spent = PlacedBid.objects.filter(
            user=self.request.user
        ).aggregate(total=Sum('amount'))
        response['total_spent'] = total_spent['total']
        return Response(response, status=status.HTTP_200_OK)