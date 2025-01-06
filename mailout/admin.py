from django.contrib import admin
from django.contrib import admin
from .models import Clients, Message, Mailout, Attempt


@admin.register(Clients)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'notes')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at')
    search_fields = ('subject', 'created_at')


@admin.register(Mailout)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'status')
    search_fields = ('status', 'message')


@admin.register(Attempt)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'emailed_at', 'status', 'server_message')
    search_fields = ('status', 'message')
