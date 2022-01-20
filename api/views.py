from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.models import *
from api.serializers import *
from api.permissions import *


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsLoggedInUserOrAdmin]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminUser]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    # A doctor can only see a list of all the patients and a specific patient instance
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsDoctorOrAdmin]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminUser]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAdminUser]


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAdminUser]


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    # Any doctor can create a visit
    # A patient can only see their own results
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsDoctorOrAdmin]
        elif self.action == 'retrieve':
            permission_classes = [IsDoctorOrAdmin | IsResultForPatient]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUser]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAdminUser]


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAdminUser]


class PatientStatesViewSet(viewsets.ModelViewSet):
    queryset = PatientStates.objects.all()
    serializer_class = PatientStatesSerializer
    permission_classes = [IsAdminUser]


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAdminUser]


class IllnessViewSet(viewsets.ModelViewSet):
    queryset = Illness.objects.all()
    serializer_class = IllnessSerializer
    permission_classes = [IsAdminUser]


class PatientIllnessesViewSet(viewsets.ModelViewSet):
    queryset = PatientIllnesses.objects.all()
    serializer_class = PatientIllnessesSerializer
    permission_classes = [IsAdminUser]


class DischargeViewSet(viewsets.ModelViewSet):
    queryset = Discharge.objects.all()
    serializer_class = DischargeSerializer
    permission_classes = [IsAdminUser]
