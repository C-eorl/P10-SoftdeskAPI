from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authentication.views import UserViewset


user_router = DefaultRouter()
user_router.register('', UserViewset, basename='users')

urlpatterns = [
    path('', include(user_router.urls)),
]