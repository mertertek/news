from django.contrib import admin
from .models import News, Comment, Like

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
admin.site.register(News, NewsAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'user','created_at']
admin.site.register(Comment, CommentAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'user', 'created_at']
admin.site.register(Like, LikeAdmin)

