from django import forms
from api.models import *


class RawPatientVisitForm(forms.Form):
    visited_patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Your ID')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    location = forms.ModelChoiceField(queryset=Address.objects.all())
    required_specialization = forms.ModelChoiceField(queryset=Specialization.objects.all())
    leading_doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label='Doctor ID')


class RawDoctorRecommendationForm(forms.Form):
    target_patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Patient ID')
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'What is it related to?',
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter the recommendation'
    }))
    to_discharge = forms.ModelChoiceField(queryset=Discharge.objects.all(), label='Confirm patient ID')


class RawDoctorMedicationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter medication name',
    }))
    dose_in_milligrams = forms.DecimalField()
    dosage_daily = forms.DecimalField()
    to_prescription = forms.ModelChoiceField(queryset=Prescription.objects.all(), label='Patient ID')


class RawDoctorStateForm(forms.Form):
    systolic_blood_pressure = forms.DecimalField()
    diastolic_blood_pressure = forms.DecimalField()
    heart_rate = forms.DecimalField()
    blood_oxygen_level = forms.DecimalField()
    to_patient_state = forms.ModelChoiceField(queryset=PatientStates.objects.all(), label='Patient ID')


class RawDoctorIllnessForm(forms.Form):
    patient_id = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Patient ID')
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter illness name',
    }))
    to_patient_illness = forms.ModelChoiceField(queryset=PatientIllnesses.objects.all(), label='Confirm patient ID')
