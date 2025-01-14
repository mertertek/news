from django.contrib import admin
from django.urls import path, include
from .views import NewsListAPIView, NewsDetailAPIView, CommentListAPIView, CommentDetailAPIView, LikeListAPIView, LikeAPIView, LikedPostListAPIView, NewsFilterAPIView, EditorNewsListAPIView, NewsListOrderByDates, PageNewsListAPIView
urlpatterns = [
    path('', NewsListAPIView.as_view(), name="news_list"),
    path('<int:pk>/', NewsDetailAPIView.as_view(), name="news_detail"),
    path('comments/', CommentListAPIView.as_view(), name="comment_list"),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name="comment_detail"),
    path('likes/', LikeListAPIView.as_view(), name="like_list"),
    path('likes/<int:pk>/', LikeAPIView.as_view(), name="like_detail"),
    path('liked/', LikedPostListAPIView.as_view(), name="liked_post_list"),
    path('filter/<str:title>/', NewsFilterAPIView.as_view(), name="news_filter"),
    path('editor/<int:editor>', EditorNewsListAPIView.as_view(), name="editor_news_list"),
    path('newest/', NewsListOrderByDates.as_view(), name="news_list_order"),
    path('page/', PageNewsListAPIView.as_view(), name="page_news_list")
]
