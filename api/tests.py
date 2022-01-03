from django.test import TestCase, Client

import api.models
from api.models import *

# Create your tests here.


# Test basic operations on model instances
class SpecializationTestCase(TestCase):
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
        except api.models.Specialization.DoesNotExist:
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
