from django.db.models import Sum
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from bidding.models import PlacedBid

from .serializers import (
    UserSerializer
)


User = get_user_model()


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': {'id': token.user.id, 'email': token.user.email}})
    

class Analytics(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get(self, *args, **kwargs):
        response = {}
        total_spent = PlacedBid.objects.filter(
            user=self.request.user
        ).aggregate(total=Sum('amount'))
        response['total_spent'] = total_spent['total']
        return Response(response, status=status.HTTP_200_OK)