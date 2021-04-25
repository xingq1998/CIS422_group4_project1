from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import datetime
from .forms import ProfileForm
from .models import Profile
from clinics.models import Clinic, ScheduleTime


def home(request):
    return render(request, 'home.html', None)


def index(request):
    message = request.GET.get('message')
    return render(request, 'users/index.html', {'message': message})


def signup(request):
    return render(request, 'users/signup.html', None)


def account_signup(request):
    if request.user.is_authenticated:
        return redirect('/index/?message=account exists')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
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
        new_user = User.objects.create_user(username=username, password=password, email=email)
        new_user.profile.phone = phone
        new_user.save()
        return render(request, 'users/login.html')
    return render(request, 'users/signup.html')


def account_login(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated:
        return redirect('/info/')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        post_dict = request.POST
        username = post_dict.get("username", "")
        email = post_dict.get("email", "")
        password = post_dict.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/info/')
    return render(request, 'users/login.html')


def account_logout(request):
    logout(request)
    return render(request, 'users/logout.html')


# user info
# need to login
@login_required(login_url='/login/')
def account_info(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        schedules = user.profile.appoint.all()
        appoints = list()
        for schedule in schedules:
            clinic = Clinic.objects.get(id=schedule.clinic_id_id)
            appoint = dict()
            appoint['id'] = schedule.id
            appoint['name'] = clinic.name
            appoint['city'] = clinic.city
            appoint['zip_code'] = clinic.zip_code
            appoint['stat'] = clinic.state
            appoint['pic_address'] = clinic.pic_address
            appoint['address'] = clinic.address
            appoint['start_time'] = schedule.start_time
            appoint['count'] = schedule.number_concurrent_appts
            appoints.append(appoint)
        return render(request, 'users/info.html', {'user': user, 'appoints': appoints})
    return redirect("/index/?message=Request Error")


@login_required(login_url='/login/')
def edit(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if request.user != user:
            return redirect('/index/?message=Permission Forbidden')
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            post_dict = request.POST
            username = post_dict.get("username", "")
            email = post_dict.get("email", "")
            phone = post_dict.get("phone", "")
            password = post_dict.get("password", "")
            if username != "":
                user.username = username
            if email != "":
                user.email = email
            if phone != "":
                user.profile.phone = phone
            if password != "":
                user.set_password(password)
            user.save()
            return render(request, 'users/info.html', {'user': user})
        else:
            return redirect('/index/?message=Error Input')

    elif request.method == 'GET':
        return render(request, 'users/edit.html', {'user': user})
    else:
        return redirect('/info/')


@login_required(login_url='/login/')
def cancel(request, id):
    if request.method == 'GET':
        profile = Profile.objects.get(user_id=request.user.id)
        profile.appoint.remove(id)
        schedtime = ScheduleTime.objects.get(pk=id)
        schedtime.number_concurrent_appts += 1
        schedtime.save()
        return redirect('/info/')
    return redirect('/info/')


@login_required(login_url='/login/')
def is_schedule(request, id):
    user = User.objects.get(request.user.id)
    appoints = user.profile.appoint.all()
    for appoint in appoints:
        if appoint.clinic_id == id:
            return True
    return False
