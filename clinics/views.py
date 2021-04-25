from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import random

from .models import Clinic, ScheduleTime
from app.models import Profile


def clinics_all(request):
    results = Clinic.objects.all()[:10]
    return render(request, "clinics/search.html", {'clinics': str(results)})


def clinics_search(request):
    if request.method == 'POST':
        post_dict = request.POST

        services = post_dict.getlist("services", "")
        ages = post_dict.getlist("ages", "")

        zipcode = post_dict.get("zipCode", "")
        state = post_dict.get("state", "")
        city = post_dict.get("city", "")
        location = post_dict.get("location", "")
        year = post_dict.get("year", "")
        month = post_dict.get("month", "")
        day = post_dict.get("day", "")
        vaccine_brand = post_dict.get("vaccineBrand", "")
        results = Clinic.objects.all()
        if zipcode != '':
            results = results.filter(zip_code=int(zipcode))
        if state != '':
            results = results.filter(state__startswith=str.lower(state))
        if city != '':
            results = results.filter(city__startswith=str.lower(city))
        if location != '':
            results = results.filter(location__contains=location)
        if year != '':
            results = results.filter(datetime__year=int(year))
        if vaccine_brand != '':
            results = results.filter(Q(phizer_stock__gt=0) | Q(moderna_stock__gt=0) | Q(janssen_stock__gt=0)) # Filter for available stock
            
        if len(services) > 0:
            if 'testing' in services:
                results = results.filter(Testing=True)
            if 'vaccination' in services:
                results = results.filter(Vaccination=True)
            if 'screening' in services:
                results = results.filter(Screening=True)
            if 'covid19Vaccination' in services:
                results = results.filter(COVID=True)
        if len(ages) > 0:
            print('ages', ages)
            if 'allAges' in ages:
                print('allAges')
                results = results.filter(All_Ages=True)
            if 'children' in ages:
                results = results.filter(Children=True)
            if 'adults' in ages:
                results = results.filter(Adults=True)
            if 'seniors' in ages:
                results = results.filter(Seniors=True)
            if 'others' in ages:
                results = results.filter(Others=True)
        return render(request, "clinics/search.html",
                      {'clinics': results, 'post_dict': post_dict})
    else:
        results = Clinic.objects.all()[:10]
        return render(request, "clinics/search.html", {'clinics': results})


def clinics_detail(request, clinic_id):
    result = Clinic.objects.get(id=clinic_id)
    return render(request, "clinics/detail.html", {'clinic_info': str(result)})


def clinics_bulk_insert(request, n_records):
    pic_address_list = [
        'https://www.ndvax.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNk1EQlE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--675d17850b4958157e947951755686414171f935/clinic2443.png',
        'https://www.ndvax.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNDhGQlE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--4517b55b198761a91ece91eddbcb2865adc8fbe6/clinic2457.png',
        'https://www.ndvax.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBeXkzQkE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--161199175c341c23a1b768f134828e570b6f26d0/clinic1656.png',
        'https://www.ndvax.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBelRJQkE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--3574f2adc48da417240d74b1c350678a40ac123e/clinic2298.png']
    instances = []
    name_list = ['Prairie Sinus Ear Allergy Clinic', 'Pembina County Health Department',
                 'Rolette County Public Health',
                 'Parshall Boys & Girls Club']
    state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'IN', 'IA', 'KS', 'KY', 'LA', 'NE', 'NV', 'NH', 'NY', 'NC', 'PA',
                  'RI',
                  'TX', 'UT', 'VT', 'VA', 'WA', 'WI', 'WY']
    city_list = ['New York City',
                 'Los Angeles',
                 'Chicago',
                 'Houston',
                 'Phoenix',
                 'Philadelphia',
                 'San Antonio',
                 'San Diego']
    stock_threshold = 100

    def random_boolean():
        return True if random.randint(0, 10) % 2 == 0 else False

    def random_pick(list):
        return list[random.randint(0, len(list) - 1)]

    for i in range(0, n_records):
        instances.append(Clinic(
            name=random_pick(name_list),
            zip_code=random.randint(0, 100000),
            state=random_pick(state_list),
            city=random_pick(city_list),
            phizer_stock=random.randint(0, stock_threshold),
            moderna_stock=random.randint(0, stock_threshold),
            janssen_stock=random.randint(0, stock_threshold),
            Testing=random_boolean(),
            Vaccination=random_boolean(),
            Screening=random_boolean(),
            COVID=random_boolean(),

            Children=random_boolean(),
            Adults=random_boolean(),
            Seniors=random_boolean(),
            Others=random_boolean(),
            All_Ages=random_boolean(),

            pic_address=random_pick(pic_address_list),
        ))
        ret = Clinic.objects.bulk_create(instances)
    return render(request, "clinics/bulk_insert.html", {'result': ret})



#-----------------Clinic Scheduler-------------#
def clinic_schedule(request, clinic_id):
    clinic = Clinic.objects.get(pk=clinic_id)
    schedule = clinic.scheduletime_set.all()
    return render(request, "clinics/schedule.html", {"schedule": schedule})


def schedule_appt(request, sched_id):
    # Get ScheduleTime from db
    sched = ScheduleTime.objects.get(id=sched_id)

    # Set response based on appt availability (handled in html)
    if sched.number_concurrent_appts > 0:
        response = 1
       
    else:
        response = 2

    # Collect information to add to context
    usr = request.user
    time = sched.start_time
    clinic = sched.clinic_id.name

    # Create context list to send to page
    context = {
           'time': time,
           'clinic': clinic,
           'resp': response,
           'usr': usr,
           'usr_prof': usr.profile,
        }
    
    # Check that user is not already scheduled and appt available
    if (usr.profile.is_scheduled == False) and (response == 1):
        # Decrement number_concurrent_appts
        sched.number_concurrent_appts -= 1
        sched.save()
        # Assign appointment to user
        usr.profile.appoint.add(sched)
        usr.profile.is_scheduled = True
        usr.profile.save()

    # Render appt schedule confirmation/error page
    return render(request, "clinics/schedule_appt.html", context)