from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Booking, ContactMessage
import json

# ============================================================
# PUBLIC PAGE VIEWS
# ============================================================

def index(request):
    """Home page view"""
    return render(request, 'index.html')

def menu(request):
    """Menu page view"""
    return render(request, 'menu.html')

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate fields
        if not all([name, email, subject, message]):
            return JsonResponse({
                'success': False, 
                'message': 'All fields are required.'
            })
        
        # Save message
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Your message has been sent successfully!'
        })
    
    return render(request, 'contact.html')


# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

def login_view(request):
    """Login page view with authentication"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate fields
        if not email or not password:
            return JsonResponse({
                'success': False, 
                'message': 'Email and password are required.'
            })
        
        try:
            # Get user by email
            user = User.objects.get(email=email)
            # Authenticate user
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True, 
                    'message': 'Login successful!'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid password.'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'User with this email does not exist.'
            })
    
    return render(request, 'login.html')

def signup_view(request):
    """Signup page view with account creation"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not all([name, email, password, confirm_password]):
            return JsonResponse({
                'success': False, 
                'message': 'All fields are required.'
            })
        
        if password != confirm_password:
            return JsonResponse({
                'success': False, 
                'message': 'Passwords do not match.'
            })
        
        if len(password) < 6:
            return JsonResponse({
                'success': False, 
                'message': 'Password must be at least 6 characters.'
            })
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False, 
                'message': 'A user with this email already exists.'
            })
        
        if User.objects.filter(username=email).exists():
            return JsonResponse({
                'success': False, 
                'message': 'Username already taken.'
            })
        
        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            user.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Account created successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'An error occurred: {str(e)}'
            })
    
    return render(request, 'signup.html')

def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('index')


# ============================================================
# PROFILE VIEWS
# ============================================================

@login_required
def profile(request):
    """User profile page with update functionality"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        bio = request.POST.get('bio')
        
        user = request.user
        
        # Update name
        if name:
            user.first_name = name
        
        # Update email
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return JsonResponse({
                    'success': False, 
                    'message': 'Email already in use by another account.'
                })
            user.email = email
            user.username = email  # Username is email
        
        user.save()
        
        # Save additional info in session (for demo purposes)
        # In production, you would use a Profile model
        request.session['phone'] = phone
        request.session['location'] = location
        request.session['bio'] = bio
        
        return JsonResponse({
            'success': True, 
            'message': 'Profile updated successfully!'
        })
    
    # Get user bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'phone': request.session.get('phone', ''),
        'location': request.session.get('location', ''),
        'bio': request.session.get('bio', ''),
    }
    
    return render(request, 'profile.html', context)

@login_required
def change_password(request):
    """Change password functionality"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        
        # Validate current password
        if not user.check_password(current_password):
            return JsonResponse({
                'success': False, 
                'message': 'Current password is incorrect.'
            })
        
        # Validate new password
        if new_password != confirm_password:
            return JsonResponse({
                'success': False, 
                'message': 'Passwords do not match.'
            })
        
        if len(new_password) < 6:
            return JsonResponse({
                'success': False, 
                'message': 'Password must be at least 6 characters.'
            })
        
        # Change password
        user.set_password(new_password)
        user.save()
        
        # Re-authenticate user to keep session alive
        login(request, user)
        
        return JsonResponse({
            'success': True, 
            'message': 'Password changed successfully!'
        })
    
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method.'
    })

@login_required
def delete_account(request):
    """Delete user account permanently"""
    if request.method == 'POST':
        user = request.user
        
        # Delete all bookings associated with the user
        Booking.objects.filter(user=user).delete()
        
        # Delete the user
        user.delete()
        
        # Logout the user
        logout(request)
        
        return JsonResponse({
            'success': True, 
            'message': 'Account deleted successfully.'
        })
    
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method.'
    })


# ============================================================
# AJAX ENDPOINTS
# ============================================================

def book_table(request):
    """Handle table booking via AJAX"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        special_requests = request.POST.get('special_requests', '')
        
        # Validate fields
        if not all([name, email, phone, date, time, guests]):
            return JsonResponse({
                'success': False, 
                'message': 'All fields are required.'
            })
        
        try:
            guests = int(guests)
            if guests < 1:
                return JsonResponse({
                    'success': False, 
                    'message': 'Number of guests must be at least 1.'
                })
        except ValueError:
            return JsonResponse({
                'success': False, 
                'message': 'Invalid number of guests.'
            })
        
        # Save booking
        booking = Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            guests=guests,
            special_requests=special_requests
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Table booked successfully!',
            'booking_id': booking.id
        })
    
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method.'
    })

@login_required
def get_user_data(request):
    """Get user data for profile via AJAX"""
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'success': True,
            'name': user.first_name,
            'email': user.email,
            'phone': request.session.get('phone', ''),
            'location': request.session.get('location', ''),
            'bio': request.session.get('bio', '')
        })
    return JsonResponse({
        'success': False, 
        'message': 'User not authenticated.'
    })

@login_required
def get_user_bookings(request):
    """Get user bookings via AJAX"""
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        bookings_data = []
        
        for booking in bookings:
            bookings_data.append({
                'id': booking.id,
                'name': booking.name,
                'email': booking.email,
                'phone': booking.phone,
                'date': booking.date.strftime('%B %d, %Y'),
                'time': booking.time.strftime('%I:%M %p'),
                'guests': booking.guests,
                'special_requests': booking.special_requests,
                'created_at': booking.created_at.strftime('%B %d, %Y')
            })
        
        return JsonResponse({
            'success': True, 
            'bookings': bookings_data
        })
    
    return JsonResponse({
        'success': False, 
        'bookings': [],
        'message': 'User not authenticated.'
    })