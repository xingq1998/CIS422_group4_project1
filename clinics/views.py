from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from .models import Clinic, ScheduleTime

# Create your views here.
def index(request):
    #
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
    context = {'state_list' : results}

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



