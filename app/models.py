from django.db import models


# just for sample, not actually used
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    create_at = models.DateTimeField('date created')
