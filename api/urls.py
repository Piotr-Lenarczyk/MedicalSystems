from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from api.views import *

router = routers.DefaultRouter()
router.register(r'specializations', SpecializationViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'users', UserViewSet)
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'results', ResultViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'patient_states', PatientStatesViewSet)
router.register(r'states', StateViewSet)
router.register(r'illnesses', IllnessViewSet)
router.register(r'discharges', DischargeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
