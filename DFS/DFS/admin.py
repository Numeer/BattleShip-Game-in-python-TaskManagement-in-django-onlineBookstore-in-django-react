from django.contrib import admin
from .models import *
from django import forms


# Register your models here.


@admin.register(UserProfile)
class authorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'profile_picture']

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" alt="{obj.user.username}" width="50" height="50" />'
        else:
            return 'N/A'

    display_profile_picture.short_description = 'Profile Picture'


@admin.register(Author)
class authorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ('name',)


@admin.register(Genre)
class genreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ('name',)


@admin.register(Book)
class bookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'display_genres']
    list_filter = ('author', 'genres')

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()]) if obj.genres.exists() else "N/A"

    display_genres.short_description = 'Genres'


@admin.register(Review)
class reviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'created_at']
    list_filter = ('user', 'book', 'created_at')


@admin.register(Rating)
class ratingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'value']
    list_filter = ('user', 'book', 'value')


@admin.register(Notification)
class notificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event_type', 'created_at', 'is_read']
    list_filter = ('user', 'event_type', 'created_at', 'is_read')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'quantity']
    list_filter = ('user', 'book')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'is_completed', 'created_at']
    list_filter = ('user', 'is_completed', 'created_at')
