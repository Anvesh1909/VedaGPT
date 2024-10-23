from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
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
    path('about_us',About,name='about_us')
]



from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)