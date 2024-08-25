from django.contrib import admin
from .models import Packet

@admin.register(Packet)
class PacketAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'source_ip', 'destination_ip', 'protocol', 'length', 'info')
