from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, UserRegisterationSerializer, UserLoginSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterationAPIView(APIView):
    permission_classes = [AllowAny]
        
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access":str(token.access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            user_serializer = CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = user_serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditorListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        editors = CustomUser.objects.filter(is_editor=True)
        serializer = CustomUserSerializer(editors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_editor=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        editor = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(editor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        editor = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(editor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        editor = get_object_or_404(CustomUser, pk=pk)
        editor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)