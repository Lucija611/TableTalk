from django.contrib import admin
from .models import Profile, Restaurant, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'sentiment', 'created_at')
    list_filter = ('sentiment', 'restaurant', 'created_at')
    search_fields = ('user__username', 'restaurant__name', 'text')