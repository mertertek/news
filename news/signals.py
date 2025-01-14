from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from .models import News, Comment, Like
from user.models import CustomUser, Editor

@receiver(post_save, sender=Like)
def update_like_count(sender, instance, created, **kwargs):
    if created:
        instance.news.like_count += 1
        instance.news.save()

@receiver(post_save, sender=News)
def update_total_post(sender, instance, created, **kwargs):
    if created:
        editor = Editor.objects.get(user=instance.editor)
        editor.total_post += 1
        editor.save()