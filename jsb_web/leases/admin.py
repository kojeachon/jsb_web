from django.contrib import admin

from jsb_web.leases.models import Lease, Room

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'type1', 'type2', 'roomnumber', 'roompeople', 'roommoney', 'created_at', 'updated_at' ]
    
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'st_date', 'ed_date', 'leasename', 'phonenumber', 'usepeople', 'phonenumber', 'contents', 'created_at', 'updated_at' ]

admin.site.register(Room, RoomAdmin)
admin.site.register(Lease, LeaseAdmin)