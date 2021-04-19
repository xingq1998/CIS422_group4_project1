from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import random

from .models import Clinic, ScheduleTime


# Create your views here.
def index(request):
    # TODO: FIGURE out how to filter this this?
    # Clinic.objects.filter()?????
    results = []
    states = []
    all_obj = Clinic.objects.all()
    for item in all_obj:
        if item.state not in states:
            states.append(item.state)
            results.append(item)

    print(results)
    context = {'state_list': results}

    return render(request, 'clinics/index.html', context)


def state(request, state):
    if state == "state":
        context = {
            'state_clinics': Clinic.objects.all(),
        }
    else:
        state_clinics = Clinic.objects.filter(state=state)
        state_time = ScheduleTime.objects.filter(clinic_id__state__contains=state)
        context = {
            'state_clinics': state_clinics,
            'state_clinics_schedules': state_time
        }

    return render(request, "clinics/state.html", context)


def clinics_all(request):
    results = Clinic.objects.all()[:10]
    return render(request, "clinics/search.html", {'clinics': str(results)})


def clinics_search(request):
    if request.method == 'POST':
        post_dict = request.POST
        services = post_dict.get("services", "")
        ages = post_dict.get("ages", "")
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
            results = results.filter(state=str.lower(state))
        if city != '':
            results = results.filter(city=str.lower(city))
        if vaccine_brand != '':
            results = results.filter(phizer_stock__gt=0)
        return render(request, "clinics/search.html", {'clinics': str(results), 'post_dict': post_dict})
    else:
        results = Clinic.objects.all()[:10]
        return render(request, "clinics/search.html", {'clinics': str(results)})


def clinics_detail(request, clinic_id):
    result = Clinic.objects.get(id=clinic_id)
    return render(request, "clinics/detail.html", {'clinic_info': str(result)})


def clinics_bulk_insert(request, n_records):
    instances = []
    state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'IN', 'IA', 'KS', 'KY', 'LA', 'NE', 'NV', 'NH', 'NY', 'NC', 'PA', 'RI',
                  'TX', 'UT', 'VT', 'VA', 'WA', 'WI', 'WY']
    city_list = []
    stock_threshold = 100
    services_list = [(Clinic.Services.COVID, Clinic.Services.Vaccination), Clinic.Services.All]
    ages_list = [(Clinic.AgeGroup.Adults, Clinic.AgeGroup.Seniors), Clinic.AgeGroup.All]
    for i in range(0, n_records):
        random_i = random.randint(0, len(state_list) - 1)
        instances.append(Clinic(zip_code=i,
                                state=state_list[random_i - 1],
                                city='pitts',
                                phizer_stock=random.randint(0, stock_threshold),
                                moderna_stock=random.randint(0, stock_threshold),
                                janssen_stock=random.randint(0, stock_threshold),
                                services=services_list[random.randint(0, 1)],
                                ages=ages_list[random.randint(0, 1)]))
    ret = Clinic.objects.bulk_create(instances)
    return render(request, "clinics/bulk_insert.html", {'result': ret})
