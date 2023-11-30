from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.forms import LoginForm, RegisterForm
from accounts.mail import send_activation_email


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You already logged in")
        return redirect("movies:movie_list")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            user = authenticate(request, email=email, password=password)
            if not user:
                messages.error(request, "Invalid username or password")
                return redirect("accounts:login")

            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 7)
            else:
                request.session.set_expiry(0)

            login(request, user)
            return redirect("movies:movie_list")
    context = {
        "form": LoginForm()
    }
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("movies:movie_list")


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You already logged in")
        return redirect("movies:movie_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            messages.info(request, 'Registration completed')
            send_activation_email(user.email)
            return redirect("accounts:login")
        else:
            return render(request, 'accounts/register.html', {'form': form})

    return render(request, 'accounts/register.html', {'form': RegisterForm()})


