from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# ------------------------------
# Models:

class Clinic(models.Model):
    name = models.CharField(max_length=30, default='Prairie Sinus Ear Allergy Clinic')
    zip_code = models.IntegerField(default=0)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=200)
    phizer_stock = models.IntegerField(default=0)
    moderna_stock = models.IntegerField(default=0)
    janssen_stock = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    Testing = models.BooleanField(default=False)
    Vaccination = models.BooleanField(default=False)
    Screening = models.BooleanField(default=False)
    COVID = models.BooleanField(default=False)

    Children = models.BooleanField(default=False)
    Adults = models.BooleanField(default=False)
    Seniors = models.BooleanField(default=False)
    Others = models.BooleanField(default=False)
    All_Ages = models.BooleanField(default=False)

    pic_address = models.CharField(max_length=300,
                                   default='https://cdn.upmc.com/-/media/upmc/campaigns/covid-vaccine/vaccineoggraphic.jpg?la=en&rev=3105491e4bd8458199540f68f6ab86f6')

    def __str__(self):
        clinic = f"""{self.address} {self.city}, {self.state} {self.zip_code}| Phizer_Stock: {self.phizer_stock} Moderna_Stock: {self.moderna_stock}"""
        return clinic

    # class Services(models.TextChoices):
    #     Testing = 'Testing', _('Testing')
    #     Vaccination = 'Vaccination', _('Vaccination')
    #     Screening = 'Screening', _('Screening')
    #     COVID = 'COVID', _('COVID')
    #     All = 'All', _('All')
    #
    # services = models.CharField(
    #     max_length=11,
    #     choices=Services.choices,
    #     default=Services.All,
    # )
    #
    # class AgeGroup(models.TextChoices):
    #     Children = 'Children', _('Children')
    #     Adults = 'Adults', _('Adults')
    #     Seniors = 'Seniors', _('Seniors')
    #     Others = 'Others', _('Others')
    #     All = 'All', _('All')
    #
    # ages = models.CharField(
    #     max_length=10,
    #     choices=AgeGroup.choices,
    #     default=AgeGroup.All,
    # )


# Clinic schedule time references a clinic_id in a many-to-one relationship
# see: https://docs.djangoproject.com/en/3.2/topics/db/models/#many-to-one-relationships
class ScheduleTime(models.Model):
    clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    number_concurrent_appts = models.IntegerField(default=0)

    def __str__(self):
        return f"""{self.clinic_id} {self.start_time} {self.number_concurrent_appts}"""

# ------------------------------
# Model Functions:
