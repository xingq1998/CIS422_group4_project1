from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json


def index(request):
    return render(request, 'home.html', None)


def signup(request):
    return render(request, 'users/signup.html', None)


def account_signup(request):
    if request.user.is_authenticated:
        return render(request, 'users/signup.html')
    if request.method == 'POST':
        post_dict = request.POST
        username = post_dict.get("username", "")
        email = post_dict.get("email", "")
        phone = post_dict.get("phone", "")
        password = post_dict.get("password", "")
        if username == "":
            return redirect("/signup")
        user = User.objects.filter(username=username)
        if user:
            return redirect("/login")
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.phone = phone
        new_user.password = password
        new_user.save()
        return render(request, 'users/login.html', {'users': new_user})
    return render(request, 'users/signup.html')


def account_login(request):
    if request.user.is_authenticated:
        return render(request, 'users/login.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        post_dict = request.POST
        username = post_dict.get("username", "")
        email = post_dict.get("email", "")
        password = post_dict.get("password", "")
        # user = authenticate(username=username, password=password)
        user = User.objects.get(username=username)
        if user is not None and user.password == password:
            login(request, user)
            return render(request, 'users/index.html')
    return render(request, 'users/login.html')


def account_logout(request):
    logout(request)
    return render(request, 'users/logout.html')


# user info
# need to login

@login_required(login_url='/login/')
def account_info(request):
    user = User.objects.get(id=request.user.id)
    user.clean_fields('password')
    u = dict()
    u['username'] = user.username
    u['email'] = user.email
    # u['phone'] = user.userprofile.phone
    return HttpResponse(json.dumps(u), content_type="application/json")