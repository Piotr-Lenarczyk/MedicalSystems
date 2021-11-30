from django.db import models


# Create your models here.


class Specialization(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    objects = models.Manager()

    class Meta:
        ordering = ['name']


class Doctor(models.Model):
    doctor_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    hospital_ward = models.CharField(max_length=50)
    specializations = models.ManyToManyField(Specialization)
    objects = models.Manager()

    class Meta:
        ordering = ['doctor_id']


class Patient(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    hospital_ward = models.CharField(max_length=50)
    date_of_admission = models.DateField()
    objects = models.Manager()

    class Meta:
        ordering = ['patient_id']


class Address(models.Model):
    address_id = models.IntegerField()
    street = models.CharField(max_length=50)
    house_number = models.IntegerField()
    apartment_number = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    objects = models.Manager()

    class Meta:
        ordering = ['postal_code']


class Visit(models.Model):
    visit_id = models.IntegerField(primary_key=True)
    visited_patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.OneToOneField(Address, on_delete=models.CASCADE)
    required_specialization = models.OneToOneField(Specialization, on_delete=models.CASCADE)
    leading_doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['visit_id']
