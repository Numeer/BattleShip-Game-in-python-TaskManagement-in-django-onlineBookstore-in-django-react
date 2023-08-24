"""
URL configuration for djangoProject3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from DFS import views
from DFS.auth import CustomAuthToken
from django.conf import settings
from django.conf.urls.static import static
from DFS.views import RegisterView, LoginView, SearchView, checkout, GenreRecommendationsView, check_purchase

router = DefaultRouter()
router.register('profiles', views.UserProfileView)
router.register('user', views.UserView, basename='user')
router.register('userprofiles', views.UserProfileView)
router.register('authors', views.AuthorView)
router.register('genres', views.GenreView)
router.register('books', views.BookView)
router.register('reviews', views.ReviewView, basename='review')
router.register('notifications', views.NotificationView)
router.register('orders', views.OrderView)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(router.urls)),
                  path('auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('gettoken/', CustomAuthToken.as_view()),
                  path('search/', SearchView.as_view(), name='search'),
                  path('order/<int:order_id>/', views.get_order_details, name='get_order_details'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('genre_recommendations/', GenreRecommendationsView.as_view(), name='genre-recommendations'),
                  path('topSelling/', views.TopSellingBookView.as_view(), name='top-selling-book'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('check-purchase/<int:book_id>/<str:username>', views.check_purchase, name='check-purchase'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
