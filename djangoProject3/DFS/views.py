from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status,  filters
from rest_framework.views import APIView
from .serializer import *
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.models import Token
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
import json
from django.db.models import Avg

# Create your views here.

stripe.api_key = settings.STRIPE_KEY


@csrf_exempt
def checkout(request):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        items = data.get('items', [])
        total_price = data.get('total_price', 0)
        username = data.get('username')
        bookId = data.get('bookId', [])
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})

        order = Order.objects.create(
            user=user,
            total_price=total_price,
        )

        line_items = []
        if isinstance(bookId, int):
            bookId = [bookId]
        for bookId, item in zip(bookId, items):
            book = Book.objects.get(id=bookId)
            line_items.append({
                'price': item['id'],
                'quantity': item['quantity']
            })
            order_item = OrderItem.objects.create(
                order=order,
                book=book,
                price=book.price,
                quantity=item['quantity'],
            )
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
        )
        return JsonResponse({'url': session.url, 'order_id': order.id})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)

        response_data = {
            'message': 'Registration failed.',
            'errors': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": serializer.data,
                "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserProfileView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class AuthorView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^title', '^genres__name', '^author__name']


class ReviewView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.request.query_params.get('book')
        if book_id:
            book_id = book_id.rstrip('/')
            try:
                book_id = int(book_id)
            except ValueError:
                return Review.objects.none()

            return Review.objects.filter(book_id=book_id)

            return Review.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class OrderView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class SearchView(generics.ListAPIView):
    search_fields = ['title', 'author__name', 'genres__name']
    filter_backends = [SearchFilter]
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer


def get_order_details(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    order_data = {
        'id': order.id,
        'status': order.status,
        'total_price': order.total_price,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

    return JsonResponse(order_data)


class GenreRecommendationsView(APIView):
    def get(self, request, *args, **kwargs):
        genre_names = request.GET.get('genre', '').split(',')
        recommended_books = Book.objects.filter(genres__name__in=genre_names).annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')[:5]
        recommendations = [
            {
                'id': book.id,
                'title': book.title,
                'author': book.author.name,
                'price': book.price,
                'price_id': book.price_id,
                'avg_rating': book.avg_rating,
            }
            for book in recommended_books
        ]
        return Response(recommendations, status=status.HTTP_200_OK)


class TopSellingBookView(APIView):
    def get(self, request, *args, **kwargs):
        top_selling_book = Book.objects.annotate(order_count=Count('orderitem')).order_by('-order_count').first()

        if top_selling_book:
            top_selling_book_data = {
                'id': top_selling_book.id,
                'title': top_selling_book.title,
                'author': top_selling_book.author.name,
                'price': top_selling_book.price,
                'price_id': top_selling_book.price_id,
            }
            return Response(top_selling_book_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No top-selling book found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def check_purchase(request, book_id, username):
    try:
        user = User.objects.get(username=username)
        purchased = OrderItem.objects.filter(order__user=user.id, book__id=book_id).exists()
        return Response({'hasPurchased': purchased})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except OrderItem.DoesNotExist:
        return Response({'hasPurchased': False})
    except Exception as e:
        return Response({'error': str(e)}, status=500)