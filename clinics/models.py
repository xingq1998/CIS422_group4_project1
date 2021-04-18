from django.db import models
from enum import Enum
from django.db.models.functions import Length, Upper


# ------------------------------
# Models: 
class Clinic(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField(default=0)
    phizer_stock = models.IntegerField(default=0)
    moderna_stock = models.IntegerField(default=0)

    def __str__(self):
        clinic = f"""{self.address} {self.city}, {self.state} {self.zip_code}| Phizer_Stock: {self.phizer_stock} Moderna_Stock: {self.moderna_stock}"""
        return clinic


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

