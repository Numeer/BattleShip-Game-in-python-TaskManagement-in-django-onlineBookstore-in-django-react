"""
URL configuration for TaskManagement project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='home'),
    path('', signup_page.as_view(), name='signup'),
    path('login/', login_page.as_view(), name='login'),
    path('logout/', logout_page.as_view(), name='logout'),
    path('taskCreate/', create_task.as_view(), name='create'),
    path('taskList', task_list_view.as_view(), name='list'),
    path('task/<int:task_id>/', task_detail.as_view(), name='details'),
    path('task/<int:task_id>/update/', update_task.as_view(), name='update'),
    path('task/<int:task_id>/delete/', delete_task.as_view(), name='delete'),
    path('task/<int:task_id>/add_comment/', add_comment.as_view(), name='addComment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# hamza : 123hamz@
# numeer: 123
# nomi: 123
# Ali raza: ali
# rehman: 1234
