from rest_framework import serializers
from API.API.models import Doctor, Patient, Specialization, Address, Visit


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'first_name', 'last_name', 'hospital_ward', 'specializations']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['name']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'hospital_ward', 'date_of_admission']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'street', 'house_number', 'apartment_number', 'city', 'postal_code', 'state', 'country']


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['visit_id', 'visited_patient', 'date', 'time', 'location', 'required_specialization', 'leading_doctor']
