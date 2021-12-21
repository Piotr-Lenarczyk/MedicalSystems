import requests
from rest_framework import serializers

from api.models import *


def request_currency_rate(currency):
    if currency == 'PLN':
        return 1.0
    request = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/' + str(currency) + '/')
    if request.status_code == 200:
        json = request.json()
        rate = json['rates'][0]['mid']
        return 1.0 / rate
    else:
        return 0.0


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('title', 'address', 'country', 'city', 'zip', 'hospital_ward')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile', 'is_doctor', 'is_patient')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.is_doctor = profile_data.get('is_doctor', profile.is_doctor)
        profile.is_patient = profile_data.get('is_patient', profile.is_patient)
        profile.title = profile_data.get('title', profile.title)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.hospital_ward = profile_data.get('hospital_ward', profile.hospital_ward)
        profile.save()

        return instance


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['name']


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserProfileSerializer(required=True)
    specializations = SpecializationSerializer(required=False)

    class Meta:
        model = Doctor
        fields = ['doctor_id', 'email', 'user', 'specializations']

    def create(self, validated_data):
        data = validated_data.pop('user')
        data2 = validated_data.pop('specializations')
        user = UserProfileSerializer.create(UserProfileSerializer(), validated_data=data)
        specializations = SpecializationSerializer.create(SpecializationSerializer(), data2)
        doctor = Doctor.objects.update_or_create(user=user, specializations=specializations)
        return doctor


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    user = UserProfileSerializer(required=True)

    class Meta:
        model = Patient
        fields = ['patient_id', 'email', 'user', 'date_of_admission']

    def create(self, validated_data):
        data = validated_data.pop('user')
        user = UserProfileSerializer.create(UserProfileSerializer(), validated_data=data)
        patient = Patient.objects.update_or_create(user=user, date_of_admission=validated_data.pop('date_of_admission'))
        return patient


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'street', 'house_number', 'apartment_number', 'city', 'postal_code', 'state', 'country']


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    visited_patient = PatientSerializer(required=True)
    location = AddressSerializer(required=False)
    required_specialization = SpecializationSerializer(required=False)
    leading_doctor = DoctorSerializer(required=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Visit
        fields = ['visit_id', 'fee', 'price', 'visited_patient', 'date', 'time', 'location', 'required_specialization',
                  'leading_doctor']

    def get_price(self, instance):
        return instance.fee * request_currency_rate(instance.visited_patient.user.country.currency)

    def create(self, validated_data):
        data1 = validated_data.pop('visited_patient')
        data2 = validated_data.pop('location')
        data3 = validated_data.pop('required_specialization')
        data4 = validated_data.pop('leading_doctor')
        visited_patient = PatientSerializer.create(PatientSerializer(), validated_data=data1)
        location = AddressSerializer.create(AddressSerializer(), validated_data=data2)
        required_specialization = SpecializationSerializer.create(SpecializationSerializer(), validated_data=data3)
        leading_doctor = DoctorSerializer.create(DoctorSerializer(), validated_data=data4)
        visit = Visit.objects.update_or_create(visited_patient=visited_patient, location=location,
                                               required_specialization=required_specialization,
                                               leading_doctor=leading_doctor)
        return visit


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['result_id', 'target_patient', 'subject', 'description']


class CountrySerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['country_assigned', 'currency', 'rate', 'last_update']

    def get_rate(self, instance):
        return request_currency_rate(instance.currency)
