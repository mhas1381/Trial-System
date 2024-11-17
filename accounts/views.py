from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from .models import User, Profile

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # اعتبارسنجی کاربر
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('exam:exam',)  # به صفحه اصلی یا داشبورد هدایت شود
            else:
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Invalid phone number or password.')

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        if not phone_number or not first_name or not last_name or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/signup.html')

        try:
            with transaction.atomic():
                user = User.objects.create_user(phone_number=phone_number, password=password)
                user.is_verified = True  # در صورت نیاز
                user.save()

                # ایجاد پروفایل
                Profile.objects.create(user=user, first_name=first_name, last_name=last_name)

            messages.success(request, 'Sign-up successful! You can now log in.')
            return redirect('accounts:login')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error occurred during sign-up.')

    return render(request, 'accounts/signup.html')