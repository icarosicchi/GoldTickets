from django.contrib import admin
from .models import Event, Category, Comment, Ticket

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Ticket)