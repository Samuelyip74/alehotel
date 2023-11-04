from django.contrib import admin
from .models import Nas,Radcheck

# Register your models here.
class NasAdmin(admin.ModelAdmin):
    list_display = ('nasname','shortname','ports','secret','server','community','description')
    search_fields = ['nasname',]

admin.site.register(Nas,NasAdmin)


class RadcheckAdmin(admin.ModelAdmin):
    list_display = ('username','attribute','op','value', 'room')
    search_fields = ['username',]

admin.site.register(Radcheck,RadcheckAdmin)