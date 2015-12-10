from django.contrib import admin

from .models import (
    Customfield,
    CustomfieldValue,
    Objectcustomfieldvalues,
    Queue,
    TicketCustomfieldValue,
    Ticket,
)

admin.site.register(Customfield)
admin.site.register(CustomfieldValue)
admin.site.register(Objectcustomfieldvalues)
admin.site.register(Queue)
admin.site.register(TicketCustomfieldValue)
admin.site.register(Ticket)
