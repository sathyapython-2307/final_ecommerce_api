from django.urls import path
from .views import UserRegistrationView, register_view, login_view
from .views import profile_view, logout_view
from .views import profile_view

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # Frontend registration and login
    path('signup/', register_view, name='register-view'),
    path('login/', login_view, name='login-view'),
    path('profile/', profile_view, name='profile-view'),
    path('logout/', logout_view, name='logout-view'),
]
