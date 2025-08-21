from django.contrib.auth import logout as auth_logout
# ...existing code...

def logout_view(request):
	auth_logout(request)
	return render(request, 'accounts/logout.html')
from store.models import Order
# ...existing code...

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
	orders = Order.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'accounts/profile.html', {'user': request.user, 'orders': orders})
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

class UserRegistrationView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserRegistrationSerializer

# Frontend registration form
class RegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				email=form.cleaned_data['email'],
				password=form.cleaned_data['password']
			)
			return redirect('login-view')
	else:
		form = RegisterForm()
	return render(request, 'accounts/register.html', {'form': form})

# Frontend login form
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(
				request,
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password']
			)
			if user is not None:
				auth_login(request, user)
				return redirect('product-list-view')
	else:
		form = LoginForm()
	return render(request, 'accounts/login.html', {'form': form})
from django.shortcuts import render

# Create your views here.
