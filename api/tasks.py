from api.models import *
from api.serializers import request_currency_rate
import datetime


def update_rates():
    for country in Country.objects.all():
        country.rate = request_currency_rate(country.currency)
        country.last_update = datetime.datetime.now()
        country.save()


def update_discharge():
    patients = Patient.objects.all()
    for patient in patients:
        if Discharge.objects.filter(patient_id=patient.id).exists():
            print("Patient found")
        else:
            Discharge.objects.create(patient_id=patient.id)
            discharge = Discharge.objects.get(patient_id=patient.id)
            Prescription.objects.create(patient_id=patient, to_discharge=discharge)
            PatientStates.objects.create(patient_id=patient.id)
            PatientIllnesses.objects.create(patient_id=patient, to_discharge=discharge)
