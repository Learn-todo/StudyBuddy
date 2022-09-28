from django.contrib import admin
from .models import Room,Message,Topic

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    search_fields = ['name', 'createdtime']
    list_display = ['name', 'createdtime']

admin.site.register(Room, RoomAdmin)
admin.site.register(Message)
admin.site.register(Topic)