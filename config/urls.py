"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('home/', home_view, name='home'),
    path('test/', test_view, name='test'),
    path('administrator/countries/', admin_country_view),
    path('administrator/addresses/', admin_address_view),
    path('administrator/users/', admin_user_view),
    path('administrator/user_profiles/', admin_user_profile_view),
    path('administrator/specializations/', admin_specialization_view),
    path('administrator/doctors/', admin_doctor_view),
    path('administrator/patients/', admin_patient_view),
    path('administrator/visits/', admin_visit_view),
    path('administrator/discharges/', admin_discharge_view),
    path('administrator/recommendations/', admin_recommendation_view),
    path('administrator/prescriptions/', admin_prescription_view),
    path('administrator/medications/', admin_medication_view),
    path('administrator/patient_states/', admin_patient_states_view),
    path('administrator/states/', admin_states_view),
    path('administrator/patient_illnesses/', admin_patient_illnesses_view),
    path('administrator/illnesses/', admin_illnesses_view),
    path('doctor/patients/', doctor_patient_view),
    path('doctor/visits/', doctor_visit_view),
    path('doctor/recommendations/', doctor_recommendation_view),
    path('doctor/prescriptions/', doctor_prescription_view),
    path('doctor/patient_states/', doctor_patient_states_view),
    path('doctor/patient_illnesses/', doctor_patient_illnesses_view),
    path('patient/discharges/', patient_discharge_view),
    path('patient/visits/', patient_visit_view),
    path('patient/book_visit/', patient_visit_create_view),
    path('doctor/create_recommendation/', doctor_recommendation_create_view),
    path('doctor/create_prescription/', doctor_medication_create_view),
    path('doctor/register_state/', doctor_state_create_view),
    path('doctor/register_illness/', doctor_illness_create_view),
]
