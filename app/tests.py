from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Booking, ContactMessage
from datetime import date, time

class BookingModelTest(TestCase):
    """Test cases for Booking model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.booking = Booking.objects.create(
            user=self.user,
            name='Test User',
            email='test@example.com',
            phone='+91 98765 43210',
            date=date(2026, 8, 25),
            time=time(19, 30),
            guests=4,
            special_requests='Window seat preferred'
        )
    
    def test_booking_creation(self):
        """Test that booking is created correctly"""
        self.assertEqual(self.booking.name, 'Test User')
        self.assertEqual(self.booking.email, 'test@example.com')
        self.assertEqual(self.booking.guests, 4)
        self.assertEqual(self.booking.user, self.user)
    
    def test_booking_str_method(self):
        """Test the string representation of booking"""
        expected_str = f"{self.booking.name} - {self.booking.date} at {self.booking.time} ({self.booking.guests} guests)"
        self.assertEqual(str(self.booking), expected_str)
    
    def test_booking_summary(self):
        """Test the booking summary method"""
        summary = self.booking.get_booking_summary()
        self.assertIn('Test User', summary)
        self.assertIn('August 25, 2026', summary)
    
    def test_booking_without_user(self):
        """Test booking creation without a user"""
        booking_no_user = Booking.objects.create(
            name='Guest User',
            email='guest@example.com',
            phone='+91 98765 43210',
            date=date(2026, 8, 26),
            time=time(20, 0),
            guests=2
        )
        self.assertIsNone(booking_no_user.user)
        self.assertEqual(booking_no_user.name, 'Guest User')


class ContactMessageModelTest(TestCase):
    """Test cases for ContactMessage model"""
    
    def setUp(self):
        """Set up test data"""
        self.message = ContactMessage.objects.create(
            name='Test Sender',
            email='sender@example.com',
            subject='Test Subject',
            message='This is a test message content that is long enough to test the preview method.'
        )
    
    def test_message_creation(self):
        """Test that message is created correctly"""
        self.assertEqual(self.message.name, 'Test Sender')
        self.assertEqual(self.message.email, 'sender@example.com')
        self.assertEqual(self.message.subject, 'Test Subject')
    
    def test_message_str_method(self):
        """Test the string representation of message"""
        expected_str = f"{self.message.name} - {self.message.subject} ({self.message.created_at.strftime('%Y-%m-%d')})"
        self.assertEqual(str(self.message), expected_str)
    
    def test_message_preview(self):
        """Test the message preview method"""
        preview = self.message.get_message_preview()
        self.assertTrue(preview.endswith('...'))
        self.assertTrue(len(preview) <= 53)  # 50 + 3 dots


class ViewTests(TestCase):
    """Test cases for views"""
    
    def test_index_page(self):
        """Test that index page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_menu_page(self):
        """Test that menu page loads correctly"""
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
    
    def test_about_page(self):
        """Test that about page loads correctly"""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_contact_page(self):
        """Test that contact page loads correctly"""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
    
    def test_login_page(self):
        """Test that login page loads correctly"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_signup_page(self):
        """Test that signup page loads correctly"""
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_profile_page_redirects_if_not_logged_in(self):
        """Test that profile page redirects if user is not logged in"""
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_login_functionality(self):
        """Test user login functionality"""
        # Create user
        User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Test login
        response = self.client.post('/login/', {
            'email': 'test2@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        # Check if login was successful through JSON response
        import json
        data = json.loads(response.content)
        self.assertTrue(data['success'])
    
    def test_signup_functionality(self):
        """Test user signup functionality"""
        response = self.client.post('/signup/', {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertEqual(response.status_code, 200)
        import json
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        # Check if user was created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())