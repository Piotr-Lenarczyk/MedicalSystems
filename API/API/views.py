from django.shortcuts import render
from rest_framework import viewsets, permissions
from API.API.models import Doctor, Patient
from API.API.serializers import DoctorSerializer, PatientSerializer


# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
