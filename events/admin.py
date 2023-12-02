from django.contrib import admin
from .models import Event, Category, Comment

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Comment)