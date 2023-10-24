from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.urls import re_path as url
from .views import index, booking

urlpatterns = [
    path('booknow/<str:startdate>/<str:enddate>/<str:guest>/<int:pk>/', booking, name='booking'),
    path('accounts/', include('allauth.urls')),    
    path('admin/', admin.site.urls),
    url(r'^$', index, name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)