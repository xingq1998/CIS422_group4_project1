from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

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
        return render(request, "clinics/search.html", {'clinics': str(results)})
    else:
        results = Clinic.objects.all()[:10]
        return render(request, "clinics/search.html", {'clinics': str(results)})


def clinics_detail(request, clinic_id):
    result = Clinic.objects.get(id=clinic_id)
    return render(request, "clinics/detail.html", {'clinic_info': str(result)})
