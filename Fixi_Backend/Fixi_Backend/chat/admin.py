from django.contrib import admin
from .models import Conversation
from .models import Message


# Register your models here.
@admin.register(Conversation)
@admin.register(Message)
class ChatAdmin(admin.ModelAdmin):
    pass