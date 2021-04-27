"""
--------------------------
Prior to running, need to run the following commands.

$ python manage.py makemigrations
$ python manage.py migrate 
-----------------------------------------

This adds rows to the database with the data from the 
Test/input_clinics.csv file for testing purposes.


Usage:
    $ python upliadTestData.py



TODO: Fix this warning.
# >>>>>>>>>
# RuntimeWarning: DateTimeField ScheduleTime.start_time received
# a naive datetime (2021-04-26 08:00:00) while time zone support is active.
# >>>>>>>>>>


WARNING: The following removes all entries from tables. 
Usefule if a fresh start is needed.
On command line: manage.py flush   



"""
# Need to setup the django enviornment, so the setting module can be located.
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django

django.setup()

import datetime
from enum import IntEnum
from clinics.models import ScheduleTime, Clinic

# CSV input file for clinic locations.
CLINIC_INPUT_FILE = r"Test/input_clinics_update.csv"


class InputHeaders(IntEnum):
    Name = 0
    ADDRESS = 1
    CITY = 2
    STATE = 3
    ZIPCODE = 4
    PHIZER_STOCK = 5
    MODERNA_STOCK = 6
    janssenStock = 7


def createClinic(data_list):
    clinic_obj = Clinic.objects.create(
        name=data_list[InputHeaders.Name],
        address=data_list[InputHeaders.ADDRESS],
        city=data_list[InputHeaders.CITY],
        state=data_list[InputHeaders.STATE],
        zip_code=data_list[InputHeaders.ZIPCODE],
        phizer_stock=int(data_list[InputHeaders.PHIZER_STOCK]),
        moderna_stock=int(data_list[InputHeaders.MODERNA_STOCK]),
        janssen_stock=int(data_list[InputHeaders.janssenStock]),
        Children=int(data_list[8]),
        Adults=int(data_list[9]),
        Seniors=int(data_list[10]),
        Others=int(data_list[11]),
        All_Ages=int(data_list[12]),
        pic_address=data_list[13],
    )

    return clinic_obj


def createSchedule(num, clinic_obj):
    """ Create num ScheduleTime for clinic_obj. """
    hour = 8
    while num > 0:
        ScheduleTime.objects.create(
            clinic_id=clinic_obj,
            start_time=datetime.datetime(2021, 4, 26, hour, 0),
            number_concurrent_appts=1
        )
        hour += 1
        num -= 1

    return None


def main():
    with open(CLINIC_INPUT_FILE, "r") as fp:
        # Ignore the headers
        fp.readline()

        for line in fp:
            data = line.rstrip().split(",")

            clin_obj = createClinic(data)

            # Set these values to int type.
            data[InputHeaders.PHIZER_STOCK] = int(data[InputHeaders.PHIZER_STOCK])
            data[InputHeaders.MODERNA_STOCK] = int(data[InputHeaders.MODERNA_STOCK])

            createSchedule(data[InputHeaders.PHIZER_STOCK], clin_obj)
            createSchedule(data[InputHeaders.MODERNA_STOCK], clin_obj)

    return None


if __name__ == "__main__":
    main()
