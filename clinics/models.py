from django.db import models
from enum import Enum
from django.db.models.functions import Length, Upper
from django.utils.translation import gettext_lazy as _


# ------------------------------
# Models: 
class Clinic(models.Model):
    zip_code = models.IntegerField(default=0)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=200)
    phizer_stock = models.IntegerField(default=0)
    moderna_stock = models.IntegerField(default=0)
    janssen_stock = models.IntegerField(default=0)

    def __str__(self):
        clinic = f"""{self.address} {self.city}, {self.state} {self.zip_code}| Phizer_Stock: {self.phizer_stock} Moderna_Stock: {self.moderna_stock}"""
        return clinic

    class Services(models.TextChoices):
        Testing = 'T', _('Testing')
        Vaccination = 'V', _('Vaccination')
        Screening = 'S', _('Screening')
        COVID = 'C', _('COVID')
        All = 'ALL', _('All')

    services = models.CharField(
        max_length=3,
        choices=Services.choices,
        default=Services.All,
    )

    class AgeGroup(models.TextChoices):
        Children = 'C', _('Children')
        Adults = 'A', _('Adults')
        Seniors = 'S', _('Seniors')
        Others = 'O', _('Others')
        All = 'ALL', _('All')

    ages = models.CharField(
        max_length=3,
        choices=AgeGroup.choices,
        default=AgeGroup.All,
    )


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
