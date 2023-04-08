from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


from .views import (
    Register,
    Login,
    Analytics
)


urlpatterns = [
    path('register/', Register.as_view(), name='create'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('analytics/', Analytics.as_view(), name='analytics'),
]