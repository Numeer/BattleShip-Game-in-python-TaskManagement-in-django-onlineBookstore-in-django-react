from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_picture', 'bio']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name')
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genres', 'price', 'price_id']

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    book = serializers.CharField(source='book.title')

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'text', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        book_tit = validated_data['book']
        text = validated_data['text']

        book = Book.objects.get(title=book_tit['title'])

        review = Review.objects.create(user=user, book=book, text=text)
        return review


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    book = serializers.CharField(source='book.title')

    class Meta:
        model = Rating
        fields = ['id', 'user', 'book', 'rating']

    def create(self, validated_data):
        user = self.context['request'].user
        book_tit = validated_data['book']
        rating_value = validated_data['rating']

        book = Book.objects.get(title=book_tit['title'])

        existing_rating = Rating.objects.filter(user=user, book=book).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
            return existing_rating

        rating = Rating.objects.create(user=user, book=book, rating=rating_value)
        return rating


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'event_type', 'message', 'created_at', 'is_read']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    is_completed = serializers.BooleanField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'is_completed', 'created_at']

    def get_items(self, obj):
        return [item.book.title for item in obj.items.all()]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('book', 'price', 'quantity')