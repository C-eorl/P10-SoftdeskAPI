import jwt
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import CustomUser
from authentication.serializers import UserSerializer, SignupSerializer


class UserViewset(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login']:
            return [AllowAny()]
        return [IsAuthenticated(), ]


    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request, *args, **kwargs):
        data = request.data
        serializer = SignupSerializer(data= data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': SignupSerializer(user).data,
            'message': 'Inscription réussie'
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'patch', 'put', 'delete'], url_path='profile')
    def profile(self, request, *args, **kwargs):
        user = request.user

        if request.method == 'GET':
            return Response(
                self.get_serializer(user).data)

        if request.method == 'PUT':
            serializer = self.get_serializer(
                user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'Profil mis à jour'
            }, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'user' : serializer.data,
                'message' : 'Profil mis à jour'
            },status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            user.delete()
            return Response({
                'message' : 'Le compte a été supprimé'
            },status=status.HTTP_204_NO_CONTENT)

