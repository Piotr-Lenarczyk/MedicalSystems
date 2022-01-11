from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class Country(models.Model):
    country_assigned = models.CharField(max_length=3, primary_key=True)
    currency = models.CharField(max_length=3)
    last_update = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = ['country_assigned']


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField('email address', unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, unique=False)
    city = models.CharField(max_length=50)
    zip = models.CharField(verbose_name='ZIP code', max_length=6)
    hospital_ward = models.CharField(max_length=50)
    objects = models.Manager()


class Specialization(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    objects = models.Manager()

    class Meta:
        ordering = ['name']


class Doctor(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, to_field='email')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    specializations = models.ManyToManyField(Specialization)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Patient(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, to_field='email')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    date_of_admission = models.DateField()
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Address(models.Model):
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
    visited_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, unique=False)
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Address, on_delete=models.CASCADE, unique=False)
    required_specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, unique=False)
    leading_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, unique=False)
    fee = models.FloatField(default=0.0)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Result(models.Model):
    target_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    objects = models.Manager()

    class Meta:
        ordering = ['id']
