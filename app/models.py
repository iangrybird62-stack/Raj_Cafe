from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Booking(models.Model):
    """
    Model to store table booking information
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='bookings',
        help_text="User who made the booking (if authenticated)"
    )
    name = models.CharField(
        max_length=100,
        help_text="Full name of the person making the booking"
    )
    email = models.EmailField(
        help_text="Email address for booking confirmation"
    )
    phone = models.CharField(
        max_length=15,
        help_text="Contact phone number"
    )
    date = models.DateField(
        help_text="Date of the booking"
    )
    time = models.TimeField(
        help_text="Time of the booking"
    )
    guests = models.IntegerField(
        help_text="Number of guests"
    )
    special_requests = models.TextField(
        blank=True, 
        null=True,
        help_text="Any special requests or occasions"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the booking was created"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.name} - {self.date} at {self.time} ({self.guests} guests)"
    
    def get_booking_summary(self):
        """Returns a formatted summary of the booking"""
        return f"Booking for {self.name} on {self.date.strftime('%B %d, %Y')} at {self.time.strftime('%I:%M %p')}"


class ContactMessage(models.Model):
    """
    Model to store contact form messages
    """
    name = models.CharField(
        max_length=100,
        help_text="Full name of the sender"
    )
    email = models.EmailField(
        help_text="Email address of the sender"
    )
    subject = models.CharField(
        max_length=200,
        help_text="Subject of the message"
    )
    message = models.TextField(
        help_text="The actual message content"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the message was sent"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def get_message_preview(self):
        """Returns a preview of the message (first 50 characters)"""
        return self.message[:50] + '...' if len(self.message) > 50 else self.message