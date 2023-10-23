from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id','user','start_date','end_date','guest','price')
    search_fields = ['name',]

admin.site.register(Reservation,ReservationAdmin)