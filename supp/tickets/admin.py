from django.contrib import admin

from .models import Message, Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message)
