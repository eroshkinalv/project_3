from django.contrib import admin
from .models import Clients, Message, Mailout, Attempt, Home


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'notes')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at')
    search_fields = ('subject', 'created_at')


@admin.register(Mailout)
class MailoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'status')
    search_fields = ('status', 'message')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'emailed_at', 'status', 'server_message')
    search_fields = ('status', 'message')


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_mailout', 'total_active', 'total_users')
    search_fields = ('total_users', 'id')
