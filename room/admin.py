from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','number','room_type','is_active')
    search_fields = ['number',]

admin.site.register(Room,RoomAdmin)
