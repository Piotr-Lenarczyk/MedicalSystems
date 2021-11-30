from rest_framework.routers import DefaultRouter
from API.API import views

router = DefaultRouter()

router.register(r'doctors', views.DoctorViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'visit', views.VisitViewSet)
router.register(r'specialization', views.SpecializationViewSet)
router.register(r'address', views.AddressViewSet)
