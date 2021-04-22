import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()

from clinics.models import ScheduleTime
from app.models import User

import datetime


def schedAppt(user, sched_obj):
    """
    This function will determine if the sched_obj time is available and,
    if so, schedule the user for that time. It will decrement number of 
    concurrent appt's available and assign the corresponding datetime to 
    the user's appt_time attribute.

    inputs:
        user: this is a User object from the database
        sched_obj: this is a ScheduleTime object from the database

    outputs:
        the function returns an integer value reflecting the terminating status
        of the function. -1 indicates the ScheduleTime is not available in the
        database. -2 indicates the user is already scheduled for an appointment
        and cannot be scheduled for another. 1 indicates success.
    """

    # Check that user is not already scheduled, and that appointments are avail
    if user.is_scheduled == True:
        return -2
    
    if sched_obj.number_concurrent_appts == 0:
        return -1

    # Decrement number of concurrent appts available, assign ScheduleTime to User
    sched_obj.number_concurrent_appts -= 1
    user.appt_time = sched_obj

    return 1


def cancelAppt(user):
    """
    This function will (if applicable) unlink a scheduled appointment from a user's account. 
    It will also incremement the number of concurrent appointments available for that ScheduleTime
    in the database so that it becomes available once more for other users.
    
    inputs:
        user: This is a User object from the database

    outputs:
        The function returns an integer value. -1 indicates the user has no appt_time 
        associated with their account. 1 indicates success.
    """
    if user.appt_time is None:
        return -1

    # Unlink ScheduleTime from User
    schedtime = user.appt_time
    user.appt_time = None

    # Check that the date is still relevant; it is possible the date has passed
    if schedtime.start_time > datetime.today().date():
        # Increment concurrent appt's for ScheduleTime
        schedtime.number_concurrent_appts += 1

    return 1