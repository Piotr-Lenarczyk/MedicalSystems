from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from api.views import *

router = routers.DefaultRouter()
router.register(r'Users', UserViewSet)
router.register(r'Doctors', DoctorViewSet)
router.register(r'Patients', PatientViewSet)
router.register(r'Specializations', SpecializationViewSet)
router.register(r'Address', AddressViewSet)
router.register(r'Visits', VisitViewSet)
router.register(r'Results', ResultViewSet)
router.register(r'Countries', CountryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
