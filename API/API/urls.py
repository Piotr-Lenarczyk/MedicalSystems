from rest_framework.routers import DefaultRouter
from API.API import views

router = DefaultRouter()

router.register(r'doctors', views.DoctorViewSet)
router.register(r'patients', views.PatientViewSet)