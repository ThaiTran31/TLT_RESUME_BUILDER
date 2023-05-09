from django.http import Http404
from django.contrib.auth.models import User, BaseUserManager
from django.conf import settings

from google.auth.transport import requests
from google.oauth2 import id_token

from rest_framework import generics, permissions, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class BlackListTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(data={'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_instance = User.objects.get(id=request.user.id)
            user_serializer = UserSerializer(user_instance)
        except User.DoesNotExist:
            raise Http404
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class UserProfileUpdate(APIView):
    permissions = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):
        try:
            user_instance = User.objects.get(id=request.user.id)
            profile_instance = user_instance.profile
            profile_key_list = ["avatar", "phone", "address", "city", "country"]
            for key in profile_key_list:
                if key in request.data.keys():
                    setattr(profile_instance, key, request.data.get(key, getattr(profile_instance, key)))
                    profile_instance.save()
        except User.DoesNotExist:
            raise Http404
        user_serializer = UserSerializer(user_instance, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthenticate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        auth_token = request.data["auth_token"]
        client_id = settings.GOOGLE_CLIENT_ID
        idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise exceptions.AuthenticationFailed("The token is either invalid or has expired")
        if idinfo["aud"] != client_id:
            raise exceptions.AuthenticationFailed("Authentication Failed")
        try:
            user = User.objects.get(email=idinfo["email"])
        except User.DoesNotExist:
            user_data = {
                "username": idinfo["email"],
                "email": idinfo["email"],
                "password": BaseUserManager().make_random_password()
            }
            user_serializer = RegisterSerializer(data=user_data)
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class LinkedinAuthenticate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        return Response({}, status=status.HTTP_200_OK)


class MockUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializers = RegisterSerializer(data=request.data, many=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
