from django.contrib import admin
from django.urls import path
from .views import UserRegisterationAPIView, UserLoginAPIView, EditorListAPIView, EditorDetailAPIView
urlpatterns = [
    path('register/', UserRegisterationAPIView.as_view(), name="register"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('editors/', EditorListAPIView.as_view(), name="editors"),
    path('editors/<int:pk>/', EditorDetailAPIView.as_view(), name="editor"),
]
