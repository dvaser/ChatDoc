from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Message, Document, Card, CustomUser

admin.site.register(Message)
admin.site.register(Document)
admin.site.register(Card)
admin.site.register(CustomUser)