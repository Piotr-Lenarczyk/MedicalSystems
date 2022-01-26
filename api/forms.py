from django import forms
from api.models import *


class PatientVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['visited_patient', 'date', 'time', 'location', 'required_specialization', 'leading_doctor']


class RawPatientVisitForm(forms.Form):
    visited_patient = forms.ModelChoiceField(queryset=Patient.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    location = forms.ModelChoiceField(queryset=Address.objects.all())
    required_specialization = forms.ModelChoiceField(queryset=Specialization.objects.all())
    leading_doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())


class RawDoctorRecommendationForm(forms.Form):
    target_patient = forms.ModelChoiceField(queryset=Patient.objects.all())
    subject = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    to_discharge = forms.ModelChoiceField(queryset=Discharge.objects.all())


class RawDoctorMedicationForm(forms.Form):
    name = forms.CharField()
    dose_in_milligrams = forms.DecimalField()
    dosage_daily = forms.DecimalField()
    to_prescription = forms.ModelChoiceField(queryset=Prescription.objects.all())


class RawDoctorStateForm(forms.Form):
    systolic_blood_pressure = forms.DecimalField()
    diastolic_blood_pressure = forms.DecimalField()
    heart_rate = forms.DecimalField()
    blood_oxygen_level = forms.DecimalField()
    to_patient_state = forms.ModelChoiceField(queryset=PatientStates.objects.all())


class RawDoctorIllnessForm(forms.Form):
    patient_id = forms.ModelChoiceField(queryset=Patient.objects.all())
    name = forms.CharField()
    to_patient_illness = forms.ModelChoiceField(queryset=PatientIllnesses.objects.all())
