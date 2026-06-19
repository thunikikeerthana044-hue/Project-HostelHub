# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, ProfileUpdateForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('hostel_list')

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to HostelHub, {user.first_name}!")
            # Send to different pages based on role
            if user.profile.role == 'owner':
                return redirect('owner_dashboard')
            return redirect('hostel_list')
        else:
            messages.error(request, "Please fix the errors below.")

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('hostel_list')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    profile = request.user.profile
    form    = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Also update User fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name  = form.cleaned_data['last_name']
            request.user.email      = form.cleaned_data['email']
            request.user.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})