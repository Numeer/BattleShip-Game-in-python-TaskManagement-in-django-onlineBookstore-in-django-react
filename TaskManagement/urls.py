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
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('logout/', views.logout_page, name='logout'),
    path('taskCreate/', views.create_task, name='create'),
    path('taskList', views.task_list_view, name='list'),
    path('task/<int:task_id>/', views.task_detail, name='details'),
    path('task/<int:task_id>/update/', views.update_task, name='update'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete'),
    path('task/<int:task_id>/add_comment/', views.add_comment, name='addComment'),
    # path('task/<int:task_id>/upload/', views.upload_attachment, name='uploadAttachment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# hamza : 123hamz@
# numeer: 123
# nomi: 123
# Ali raza: ali
# rehman: 1234
