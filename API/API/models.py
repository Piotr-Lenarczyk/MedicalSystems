from django.db import models

# Create your models here.


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    hospital_ward = models.CharField(max_length=50)
    expertise = models.CharField(max_length=40)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    hospital_ward = models.CharField(max_length=50)
    date_of_admission = models.DateField()
    objects = models.Manager()

    class Meta:
        ordering = ['id']
