"""
URL configuration for VedaGPT project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from models.views import index ,send,clear_records,viewFile,SignupPage,LoginPage,LogoutPage,getHistory,createChat,model
from models.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('send', send, name='send'),
    path('clear_records',clear_records,name='clear_records'),
    path('viewFile/<str:fileName>/', view_file, name='view_file'),
    
    path('signup',SignupPage,name='signup'),
    path('login/',LoginPage,name='login'),
    path('logout',LogoutPage,name='logout'),
    
    path('getHistory',getHistory,name='getHistory'),
    
    path('createChat',createChat,name='createChat'),
    path('model/<int:model_no>/', model_view, name='model'),
    path('Upload',Upload,name='Upload'),
    
    path('AddModel', AddModel,name='AddModel'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)