from django.shortcuts import render
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from .models import News, Comment, Like
from .serializers import NewsSerializer, CommentSerializer, LikeSerializer
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .permissions import IsEditorUser, IsNewsOwnerOrReadOnly, IsCommentOwnerOrReadOnly, IsLikeOwner


class NewsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_editor:
            return Response({"message": "Only editors can create news"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(editor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNewsOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            self.check_object_permissions(request, news)
            serializer = NewsSerializer(news)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return Response({"message": "News not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            self.check_object_permissions(request, news)
            serializer = NewsSerializer(news, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except News.DoesNotExist:
            return Response({"message": "News not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            self.check_object_permissions(request, news)
            news.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except News.DoesNotExist:
            return Response({"message": "News not found"}, status=status.HTTP_404_NOT_FOUND)

class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCommentOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, comment)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, comment)
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

class LikeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsLikeOwner]

    def delete(self, request, pk):
        try:
            like = Like.objects.get(pk=pk)
            self.check_object_permissions(request, like)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"message": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

class LikedPostListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        liked_post = Like.objects.filter(user = request.user)

        if not liked_post.exists():
            return Response({"message":"Your liked post list is empty."}, status = status.HTTP_200_OK)            

        liked_display = []
        for liked in liked_post:
            post = liked.news
            serializer = NewsSerializer(post).data
            liked_display.append(serializer)
        return Response(liked_display, status=status.HTTP_200_OK)

class NewsFilterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, title):

        news_objects = News.objects.filter(title__icontains=title)

        if not news_objects.exists():
            return Response({"message": "News not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditorNewsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, editor):
        news = News.objects.filter(editor=editor)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class NewsListOrderByDates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PageNewsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news = News.objects.all().order_by('-created_at')
        page = request.query_params.get('page', 1)
        paginator = Paginator(news, 3) 

        try:
            paginated_news = paginator.page(page)
        except PageNotAnInteger:
            paginated_news = paginator.page(1)
        except EmptyPage:
            paginated_news = []

        serializer = NewsSerializer(paginated_news, many=True)
        return Response({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page,
            "results": serializer.data
        }, status=status.HTTP_200_OK)