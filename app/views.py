from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    return render(request, 'home.html', None)


def signup(request):
    return render(request, 'users/signup.html', None)


def account_signup(request):
    if request.user.is_authenticated:
        return render(request, 'users/signup.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        post_dict = request.POST
        username = post_dict.get("username", "")
        email = post_dict.get("email", "")
        phone = post_dict.get("phone", "")
        password = post_dict.get("password", "")
        if username == "":
            return redirect("/signup")
        if User.objects.get(username=username) is not None:
            return redirect("/login")
        new_user = User.objects.create_user(username=username, password=password, email=email)
        return render(request, 'users/login.html', {'users': new_user})
    return render(request, 'users/signup.html')


def account_login(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated:
        return render(request, 'users/login.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        post_dict = request.POST
        username = post_dict.get("username", "")
        email = post_dict.get("email", "")
        password = post_dict.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return render(request, 'users/login.html')


def account_logout(request):
    logout(request)
    return render(request, 'users/logout.html')
