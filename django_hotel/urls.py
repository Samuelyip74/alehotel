from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.urls import re_path as url
from .views import index, booking, list_rooms, check_in, check_out, check_in_out, check_in_confirmation

urlpatterns = [
    path('booknow/<str:startdate>/<str:enddate>/<str:guest>/<int:pk>/', booking, name='booking'),
    path('check_in_out/', check_in_out, name='check_in_out'),
    path('check_in/<int:pk>/', check_in_confirmation, name='check_in_confirmation'),
    path('check_in/', check_in, name='check_in'),
    path('check_out/', check_out, name='check_out'),
    path('list/', list_rooms, name='listing'),
    path('accounts/', include('allauth.urls')),    
    path('admin/', admin.site.urls),
    url(r'^$', index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)