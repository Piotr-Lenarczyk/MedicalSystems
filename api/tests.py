from django.test import TestCase, Client
from api.models import *
import datetime

# Create your tests here.


# Test basic operations on basic model instances
class BasicModelTestCase(TestCase):
    # A basic model is understood as one without relations with other models
    def setUp(self):
        Specialization.objects.create(name="Anesthesiology")
        Specialization.objects.create(name="Surgery")
        Specialization.objects.create(name="Urology")

    def testSpecializationCreation(self):
        """New Specializations are created successfully"""
        anesthesiology = Specialization.objects.get(name="Anesthesiology")
        surgery = Specialization.objects.get(name="Surgery")
        urology = Specialization.objects.get(name="Urology")
        self.assertEqual(anesthesiology.name, "Anesthesiology")
        self.assertEqual(surgery.name, "Surgery")
        self.assertEqual(urology.name, "Urology")

    def testSpecializationModification(self):
        """Specified attributes of an object are changed successfully"""
        anesthesiology = Specialization.objects.get(name="Anesthesiology")
        surgery = Specialization.objects.get(name="Surgery")
        urology = Specialization.objects.get(name="Urology")
        anesthesiology.name = "Dermatology"
        surgery.name = "Radiology"
        urology.name = "Oncology"
        self.assertEqual(anesthesiology.name, "Dermatology")
        self.assertEqual(surgery.name, "Radiology")
        self.assertEqual(urology.name, "Oncology")

    # noinspection PyUnresolvedReferences
    def testSpecializationDeletion(self):
        """Newly created Specializations are deleted successfully; trying to query for them raises DoesNotExist
        exception"""
        Specialization.objects.get(name="Anesthesiology").delete()
        Specialization.objects.get(name="Surgery").delete()
        Specialization.objects.get(name="Urology").delete()
        try:
            Specialization.objects.get(name="Anesthesiology")
            Specialization.objects.get(name="Surgery")
            Specialization.objects.get(name="Urology")
        except Specialization.DoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


# Test user authentication
class AccessTestCase(TestCase):
    def setUp(self):
        # Test database has no users by default, so a User instance must be created before attempting authentication
        User.objects.create_superuser('admin', 'admin@admin.com', 'password')

    def testURL(self):
        """No such URL exists: server returns 404 Not Found status code"""
        client = Client()
        response = client.get('/api/abc/')
        self.assertEqual(response.status_code, 404)

    def testUnauthenticatedAccess(self):
        """User is not authenticated: server returns a 401 Unauthorized status code"""
        client = Client()
        response = client.get('/api/users/')
        self.assertEqual(response.status_code, 401)

    def testAuthenticatedAccess(self):
        """User is authenticated and has proper permissions: server returns a 200 OK status code"""
        client = Client()

        # Request to an authentication endpoint; should return a 302 Found status code
        authenticate = client.post('/api/auth/login/', {'username': 'admin@admin.com', 'password': 'password'})
        self.assertEqual(authenticate.status_code, 302)

        # Attempt access to web resources, assuming provided user is a superuser (so that they have full access)
        client.login(username='admin@admin.com', password='password')
        response = client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        client.logout()


# Test basic operations on advanced model instances
class AdvancedModelTestCase(TestCase):
    # An advanced model is a model with at least one relation to another model
    def setUp(self):
        # Prerequisites
        user1 = User.objects.create_user('User1', 'email1@email.com', 'password', is_doctor=True, is_patient=False)
        user2 = User.objects.create_user('User2', 'email2@email.com', 'password', is_doctor=False, is_patient=True)
        country = Country.objects.create(country_assigned='POL', currency='PLN')
        user_profile1 = UserProfile.objects.create(user=user1, title='Doc', address='Add1', country=country,
                                                   city='Warsaw', zip='00-000', hospital_ward='ER')
        user_profile2 = UserProfile.objects.create(user=user2, title='Mr', address='Add2', country=country,
                                                   city='Warsaw', zip='00-000', hospital_ward='ER')
        doctor = Doctor.objects.create(doctor_id=1, email=user1, user=user_profile1)
        patient = Patient.objects.create(patient_id=1, email=user2, user=user_profile2, date_of_admission='2021-12-01')
        specialization = Specialization.objects.create(name='Neurology')
        address = Address.objects.create(address_id=1, street='Street', house_number=10, apartment_number=20,
                                         city='Opole', postal_code='11-111', state='Upper Silesia', country='POL')
        Visit.objects.create(visit_id=1, visited_patient=patient, date=datetime.date.today(), time=datetime.time(),
                             location=address, required_specialization=specialization, leading_doctor=doctor)

    def testValidatePrerequisites(self):
        """SetUp function was executed successfully; proper instances of models were created"""
        self.assertTrue(User.objects.get(email='email1@email.com').is_doctor)
        self.assertTrue(User.objects.get(email='email2@email.com').is_patient)
        self.assertEqual(Country.objects.get(country_assigned='POL').currency, 'PLN')
        self.assertEqual(User.objects.get(email='email1@email.com'), UserProfile.objects.get(address='Add1').user)
        self.assertEqual(User.objects.get(email='email2@email.com'), UserProfile.objects.get(address='Add2').user)
        self.assertEqual(Doctor.objects.get(doctor_id=1).user, UserProfile.objects.get(address='Add1'))
        self.assertEqual(Patient.objects.get(patient_id=1).date_of_admission, datetime.date(2021, 12, 1))
        self.assertEqual(Specialization.objects.get(name='Neurology').name, 'Neurology')
        self.assertEqual(Address.objects.get(address_id=1).state, 'Upper Silesia')

    def testVisitCreation(self):
        """A new instance of Visit model was created successfully"""
        self.assertEqual(Visit.objects.get(visit_id=1).visited_patient.date_of_admission, datetime.date(2021, 12, 1))

    def testVisitModification(self):
        """Specific attributes of a newly created instance of Visit model are changed successfully"""
        visit = Visit.objects.get(visit_id=1)
        visit.time = '09:00'
        self.assertEqual(visit.time, '09:00')
        address = Address.objects.create(address_id=2, street='Avenue', house_number=50, apartment_number=30,
                                         city='Seattle', postal_code='22-222', state='Washington', country='USA')
        visit.location = address
        self.assertEqual(visit.location.state, 'Washington')

    def testVisitDeletion(self):
        """Newly created Visit is deleted successfully; trying to query for it raises DoesNotExist exception"""
        Visit.objects.get(visit_id=1).delete()
        try:
            Visit.objects.get(visit_id=1)
        except Visit.DoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


# Check whether user has the permissions that allow access to a resource
class PermissionTestCase(TestCase):
    def setUp(self):
        # Prerequisites
        User.objects.create_superuser('admin', 'admin@admin.com', 'password')
        user1 = User.objects.create_user('user1', 'email1@email.com', 'password', first_name='Doctor', last_name='One',
                                         is_doctor=True, is_patient=False)
        user2 = User.objects.create_user('user2', 'email2@email.com', 'password', first_name='Patient', last_name='One',
                                         is_doctor=False, is_patient=True)

        country = Country.objects.create(country_assigned='POL', currency='PLN')
        user_profile1 = UserProfile.objects.create(user=user1, title='Doc', address='Add1', country=country,
                                                   city='Warsaw', zip='00-000', hospital_ward='ER')
        user_profile2 = UserProfile.objects.create(user=user2, title='Mr', address='Add2', country=country,
                                                   city='Warsaw', zip='00-000', hospital_ward='ER')
        doctor = Doctor.objects.create(doctor_id=1, email=user1, user=user_profile1)
        patient = Patient.objects.create(patient_id=1, email=user2, user=user_profile2, date_of_admission='2021-12-01')
        specialization = Specialization.objects.create(name='Neurology')
        address = Address.objects.create(address_id=1, street='Street', house_number=10, apartment_number=20,
                                         city='Opole', postal_code='11-111', state='Upper Silesia', country='POL')
        Visit.objects.create(visit_id=1, visited_patient=patient, date=datetime.date.today(), time=datetime.time(),
                             location=address, required_specialization=specialization, leading_doctor=doctor)
        Result.objects.create(result_id=1, target_patient=patient, subject='Subject', description='This is a test.')

    def testValidatePrerequisites(self):
        """User has properly logged in"""
        client = Client()

        # Login as administration personnel
        client.login(username='admin@admin.com', password='password')
        response = client.get('/api/')
        self.assertEqual(response.status_code, 200)
        client.logout()

        # Login as medical personnel
        client.login(username='email1@email.com', password='password')
        response = client.get('/api/')
        self.assertEqual(response.status_code, 200)
        client.logout()

        # Login as patient
        client.login(username='email1@email.com', password='password')
        response = client.get('/api/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    def testViewPermission(self):
        """Permissions of user are successfully verified; proper view access level is granted"""
        client = Client()

        # Access view as administration personnel
        client.login(username='admin@admin.com', password='password')
        # List out all instances in a view
        response = client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        # Retrieve a single instance in a view
        response = client.get('/api/users/1/')
        self.assertEqual(response.status_code, 200)
        # Create a new instance in a view
        response = client.post('/api/results/', {'result_id': 2, 'target_patient': 1, 'subject': 'Subject2',
                                                 'description': 'Another test'})
        self.assertEqual(response.status_code, 201)
        # Partially update existing instance in a view
        response = client.patch('/api/results/1/', {'description': 'Another TEST'}, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Result.objects.get(result_id=1).description, 'Another TEST')

        response = client.get('/api/doctors/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/api/doctors/1/')
        self.assertEqual(response.status_code, 200)
        client.logout()

        # Access view as medical personnel
        client.login(username='email1@email.com', password='password')
        # Access should be granted, returning a 200 OK status code
        response = client.get('/api/patients/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/api/patients/1/')
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/results/', {'result_id': 3, 'target_patient': 1, 'subject': 'Subject3',
                                                 'description': 'Yet another test'})
        self.assertEqual(response.status_code, 201)
        # Access should be denied, returning a 403 Forbidden status code
        response = client.get('/api/users/')
        self.assertEqual(response.status_code, 403)
        response = client.get('/api/users/1/')
        self.assertEqual(response.status_code, 403)
        response = client.post('/api/specializations/', {'name': 'ER'})
        self.assertEqual(response.status_code, 403)
        client.logout()

        # Access view as patient
        client.login(username='email2@email.com', password='password')
        # Access should be granted, returning a 200 OK status code
        response = client.get('/api/results/1/')
        self.assertEqual(response.status_code, 200)
        # Access should be denied, returning a 403 Forbidden status code
        response = client.get('/api/doctors/')
        self.assertEqual(response.status_code, 403)
        response = client.get('/api/doctors/1/')
        self.assertEqual(response.status_code, 403)
        response = client.post('/api/results/', {'result_id': 4, 'target_patient': 1, 'subject': 'Subject4',
                                                 'description': 'Yet again, another test'})
        self.assertEqual(response.status_code, 403)
        client.logout()
