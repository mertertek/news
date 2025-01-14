from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now
from user.models import CustomUser, Editor

class News(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')
    created_at = models.DateField(default=now)
    like_count = models.IntegerField(default=0)


    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateField(default=now)

    def __str__(self):
        return self.comment

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateField(default=now)

    def __str__(self):
        return self.user.name
    