from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.models import *
from api.serializers import *
from api.permissions import *
from api.forms import *


# Create your views here.

# Model-related views
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


# Frontend views
def home_view(request, *args, **kwargs):
    privilege_level = ""
    if not request.user.is_authenticated:
        privilege_level = "an anonymous user"
    else:
        if request.user.is_staff:
            privilege_level = "an administation staff member"
        elif request.user.is_doctor:
            privilege_level = "a medical staff member"
        elif request.user.is_patient:
            privilege_level = "a patient"
    context = {
        "title": "Home Page",
        "list": [1, 2, 3, 4, 5],
        "access": privilege_level
    }
    return render(request, "home.html", context)


def test_view(request, *args, **kwargs):
    addresses = Address.objects.all()
    context = {
        "model": addresses,
    }
    return render(request, "test.html", context)


def admin_country_view(request, *args, **kwargs):
    data = Country.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/countries.html", context)


def admin_address_view(request, *args, **kwargs):
    data = Address.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/addresses.html", context)


def admin_user_view(request, *args, **kwargs):
    data = User.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/users.html", context)


def admin_user_profile_view(request, *args, **kwargs):
    data = UserProfile.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/user_profiles.html", context)


def admin_specialization_view(request, *args, **kwargs):
    data = Specialization.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/specializations.html", context)


def admin_doctor_view(request, *args, **kwargs):
    data = Doctor.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/doctors.html", context)


def admin_patient_view(request, *args, **kwargs):
    data = Patient.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/patients.html", context)


def admin_visit_view(request, *args, **kwargs):
    data = Visit.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/visits.html", context)


def admin_discharge_view(request, *args, **kwargs):
    data = Discharge.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/discharges.html", context)


def admin_recommendation_view(request, *args, **kwargs):
    data = Recommendation.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/recommendations.html", context)


def admin_prescription_view(request, *args, **kwargs):
    data = Prescription.objects.all()
    medications = Medication.objects.all()
    context = {
        "model": data,
        "medications": medications,
    }
    return render(request, "admin/prescriptions.html", context)


def admin_medication_view(request, *args, **kwargs):
    data = Medication.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/medications.html", context)


def admin_patient_states_view(request, *args, **kwargs):
    data = PatientStates.objects.all()
    states = State.objects.all()
    context = {
        "model": data,
        "states": states,
    }
    return render(request, "admin/patient_states.html", context)


def admin_states_view(request, *args, **kwargs):
    data = State.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/states.html", context)


def admin_patient_illnesses_view(request, *args, **kwargs):
    data = PatientIllnesses.objects.all()
    illnesses = Illness.objects.all()
    context = {
        "model": data,
        "illnesses": illnesses
    }
    return render(request, "admin/patient_illnesses.html", context)


def admin_illnesses_view(request, *args, **kwargs):
    data = Illness.objects.all()
    context = {
        "model": data,
    }
    return render(request, "admin/illnesses.html", context)


def doctor_patient_view(request, *args, **kwargs):
    data = Patient.objects.all()
    context = {
        "model": data,
    }
    return render(request, "doctor/patients.html", context)


def doctor_visit_view(request, *args, **kwargs):
    data = Visit.objects.filter(leading_doctor__email=request.user.email)
    context = {
        "model": data,
    }
    return render(request, "doctor/visits.html", context)


def doctor_recommendation_view(request, *args, **kwargs):
    data = Recommendation.objects.all()
    context = {
        "model": data,
    }
    return render(request, "doctor/recommendations.html", context)


def doctor_prescription_view(request, *args, **kwargs):
    data = Prescription.objects.all()
    medications = Medication.objects.all()
    context = {
        "model": data,
        "medications": medications,
    }
    return render(request, "doctor/prescriptions.html", context)


def doctor_patient_states_view(request, *args, **kwargs):
    data = PatientStates.objects.all()
    states = State.objects.all()
    context = {
        "model": data,
        "states": states,
    }
    return render(request, "doctor/patient_states.html", context)


def doctor_patient_illnesses_view(request, *args, **kwargs):
    data = PatientIllnesses.objects.all()
    illnesses = Illness.objects.all()
    context = {
        "model": data,
        "illnesses": illnesses
    }
    return render(request, "doctor/patient_illnesses.html", context)


def patient_discharge_view(request, *args, **kwargs):
    data = Discharge.objects.filter(patient_id__email=request.user.email)
    medications = Medication.objects.filter(to_prescription__patient_id__email=request.user.email)
    illnesses = Illness.objects.filter(patient_id__email=request.user.email)
    recommendations = Recommendation.objects.filter(target_patient_id__email=request.user.email)
    context = {
        "model": data,
        "medications": medications,
        "illnesses": illnesses,
        "recommendations": recommendations,
    }
    return render(request, "patient/discharges.html", context)


def patient_visit_view(request, *args, **kwargs):
    data = Visit.objects.filter(visited_patient__email=request.user.email)
    context = {
        "model": data,
    }
    return render(request, "patient/visits.html", context)


def patient_visit_create_view(request):
    form = PatientVisitForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PatientVisitForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, "patient/visit_create.html", context)


def doctor_recommendation_create_view(request):
    form = DoctorRecommendationForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DoctorRecommendationForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, "doctor/recommendation_create.html", context)


def doctor_medication_create_view(request):
    form = DoctorMedicationForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DoctorMedicationForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, "doctor/prescription_create.html", context)


def doctor_state_create_view(request):
    form = DoctorStateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DoctorStateForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, "doctor/state_register.html", context)


def doctor_illness_create_view(request):
    form = DoctorIllnessForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DoctorIllnessForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, "doctor/illness_register.html", context)
