from django.urls import path

from .views import (
    ListCreateProduct,
    RetrieveUpdateDestroyProduct,
    RetrieveProduct,
    PlaceBid,
    ListUserBid,
    ListAllBid
)


urlpatterns = [
    path('list-create-product/', ListCreateProduct.as_view(), name='list-create-product'),
    path('retrieve-update-destroy-product/<str:slug>/', RetrieveUpdateDestroyProduct.as_view(), name='retrieve-update-product'),
    path('retrieve-product/<str:slug>/', RetrieveProduct.as_view(), name='retrieve-product'),
    path('place-bid/', PlaceBid.as_view(), name='place-bid'),
    path('list-user-bid/', ListUserBid.as_view(), name='list-user-bid'),
    path('list-all-bid/', ListAllBid.as_view(), name='list-all-bid'),
]