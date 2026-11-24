from django.urls import path
from . import views


urlpatterns = [
    # ============================================================
    # PUBLIC PAGES
    # ============================================================
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # ============================================================
    # AUTHENTICATION
    # ============================================================
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # ============================================================
    # USER PROFILE
    # ============================================================
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # ============================================================
    # AJAX ENDPOINTS (for form submissions and data fetching)
    # ============================================================
    path('book-table/', views.book_table, name='book_table'),
    path('get-user-data/', views.get_user_data, name='get_user_data'),
    path('get-user-bookings/', views.get_user_bookings, name='get_user_bookings'),
]