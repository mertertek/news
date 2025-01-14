from django.contrib import admin
from .models import CustomUser, Editor

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_editor', 'date_joined']
admin.site.register(CustomUser, CustomUserAdmin)

class EditorAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_post']
admin.site.register(Editor, EditorAdmin)
