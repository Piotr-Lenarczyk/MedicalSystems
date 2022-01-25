from django import forms
from api.models import *


class PatientVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['visited_patient', 'date', 'time', 'location', 'required_specialization', 'leading_doctor']


class DoctorRecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['target_patient', 'subject', 'description', 'to_discharge']


class DoctorMedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dose_in_milligrams', 'dosage_daily', 'to_prescription']


class DoctorStateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['systolic_blood_pressure', 'diastolic_blood_pressure', 'heart_rate', 'blood_oxygen_level',
                  'to_patient_state']


class DoctorIllnessForm(forms.ModelForm):
    class Meta:
        model = Illness
        fields = ['patient_id', 'name', 'to_patient_illness']
