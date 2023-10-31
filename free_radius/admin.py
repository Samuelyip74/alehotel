from django.contrib import admin
from .models import Nas

# Register your models here.
class NasAdmin(admin.ModelAdmin):
    list_display = ('nasname','shortname','ports','secret','server','community','description')
    search_fields = ['nasname',]

admin.site.register(Nas,NasAdmin)