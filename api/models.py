from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Country(models.Model):
    country_assigned = models.CharField(max_length=3, primary_key=True)
    currency = models.CharField(max_length=3)
    last_update = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = ['country_assigned']


class Address(models.Model):
    street = models.CharField(max_length=50)
    house_number = models.IntegerField()
    apartment_number = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


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
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    hospital_ward = models.CharField(max_length=50)
    objects = models.Manager()


class Specialization(models.Model):
    name = models.CharField(max_length=30)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Doctor(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, to_field='email')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Patient(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, to_field='email')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    date_of_admission = models.DateField()
    is_hospitalized = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


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


class Prescription(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Belonging to patient')
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Medication(models.Model):
    name = models.CharField(max_length=50, verbose_name='Medication name')
    dose_in_milligrams = models.IntegerField(verbose_name='Single medication dose in milligrams')
    dosage_daily = models.IntegerField(verbose_name='Daily medication dosage')
    to_prescription = models.ForeignKey(Prescription, related_name='medications', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class PatientStates(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='State of patient')
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class State(models.Model):
    systolic_blood_pressure = models.IntegerField(default=120, validators=[MinValueValidator(20), MaxValueValidator(400)])
    diastolic_blood_pressure = models.IntegerField(default=80, validators=[MinValueValidator(20), MaxValueValidator(400)])
    heart_rate = models.IntegerField(default=80, validators=[MinValueValidator(30), MaxValueValidator(220)])
    blood_oxygen_level = models.IntegerField(default=97, validators=[MinValueValidator(65), MaxValueValidator(100)],
                                             verbose_name='Blood oxygen saturation in %')
    measurement_time = models.DateTimeField(auto_now_add=True, verbose_name='Time at which state was recorded')
    to_patient_state = models.ForeignKey(PatientStates, related_name='states', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Illness(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    objects = models.Manager()

    class Meta:
        ordering = ['id']


class Discharge(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Medication, on_delete=models.CASCADE)
    illness = models.ForeignKey(Illness, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['id']
