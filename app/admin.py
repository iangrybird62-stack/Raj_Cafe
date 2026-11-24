from django.contrib import admin
from .models import Booking, ContactMessage

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'date', 'time', 'guests', 'user', 'created_at']
    list_filter = ['date', 'created_at', 'guests']
    search_fields = ['name', 'email', 'phone', 'special_requests']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('date', 'time', 'guests', 'special_requests')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )