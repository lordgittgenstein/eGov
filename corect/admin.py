from django.contrib import admin
from corect.models import Complaint, Branch, Officer, History, Message, Office, Location

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'datetime')

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'head')

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('designation', 'phone', 'email')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'detail')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'text')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('state', 'division', 'district', 'subdistrict', 'locality')

class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Officer, OfficerAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Office, OfficeAdmin)
