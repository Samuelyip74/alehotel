from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.urls import re_path as url
from .views import (
    index, 
    booking, 
    list_rooms, 
    check_in, 
    check_out, 
    check_in_out, 
    check_in_confirmation, 
    check_in_completed, 
    unlock_door,
    stellar_login,
    stellar_login_face,
    ServiceWorker,
    captive_redirect,
    guest_services,
    webhook_reservation
)

urlpatterns = [
    path('booknow/<str:startdate>/<str:enddate>/<str:guest>/<int:pk>/', booking, name='booking'),
    path('webhook/reservation/', webhook_reservation.as_view(), name='webhook_reservation'),
    path('unlock_door/', unlock_door, name='unlock_door'),
    path('check_in_out/', check_in_out, name='check_in_out'),
    path('check_in/<int:pk>/', check_in_confirmation, name='check_in_confirmation'),
    path('check_in/completed/', check_in_completed, name='check_in_completed'),
    path('check_in/', check_in, name='check_in'),
    path('check_out/', check_out, name='check_out'),
    path('list/', list_rooms, name='listing'),
    path('guest_services/', guest_services, name='guest_services'),
    path('accounts/', include('allauth.urls')),   
    path('ale/login', stellar_login, name='stellar_login'), 
    path('ale/face/login', stellar_login_face, name='stellar_login_face'), 
    path('service-worker.js', ServiceWorker.as_view(), name="sw"),
    path('captive/', captive_redirect, name="captive"),
    path('admin/', admin.site.urls),
    url(r'^$', index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)