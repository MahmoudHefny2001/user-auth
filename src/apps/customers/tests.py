from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from apps.customers.models import Customer, CustomerProfile
from rest_framework import status



class CustomerSignupTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('customer_signup')

    def test_customer_signup_success(self):
        data = {
            "full_name": "John Doe",
            "email": "johndoe@mail.com",
            "phone_number": "12345678905",
            "password": "mM-john1234",
            "address": "123, New York, USA",
        }
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['full_name'], "John Doe")
        self.assertEqual(response.data['user']['email'], "johndoe@mail.com")
        self.assertEqual(response.data['user']['phone_number'], "12345678905")
        self.assertEqual(response.data['user']['address'], "123, New York, USA")
        self.assertTrue(CustomerProfile.objects.filter(customer__email="johndoe@mail.com").exists())

    
    def test_customer_signup_invalid_data(self):
        data = {
            "full_name": "",
            "email": "invalidemail",
            "phone_number": "1234567890",
            "password": "short",
            "address": "123, New York, USA",
        }
        
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('email', response.data['error'])
        self.assertIn('full_name', response.data['error'])
        self.assertIn('phone_number', response.data['error'])
        
        self.assertIn('password', response.data['error']) 


    def test_customer_signup_missing_data(self):
        data = {
            "full_name": "John Doe",
            "email": "",
            "phone_number": "",
            "password": "",
            "address": "123, New York, USA",
        }
        
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('email', response.data['error'])
        self.assertIn('phone_number', response.data['error'])
        self.assertIn('password', response.data['error'])



class CustomerLoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            full_name="John Doe",
            email="johndoe@mail.com",
            phone_number="1234567890",
            address="123, New York, USA",
        )
        self.customer.set_password('john1234')
        self.customer.save()
        
    def test_customer_profile_creation(self):
        profile_exists = CustomerProfile.objects.filter(customer=self.customer).exists()
        self.assertTrue(profile_exists, "CustomerProfile should be created for a new Customer")
        
    def test_customer_login(self):
        login_url = reverse('customer_login')
        response = self.client.post(
            login_url,
            {
                "email_or_phone": "johndoe@mail.com",
                "password": "john1234",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data["user"]["customer"]["full_name"], "John Doe")
        self.assertEqual(response.data["user"]["customer"]["email"], "johndoe@mail.com")
        self.assertEqual(response.data["user"]["customer"]["phone_number"], "1234567890")
        self.assertEqual(response.data["user"]["customer"]["address"], "123, New York, USA")

    def test_customer_login_invalid(self):
        login_url = reverse('customer_login')
        response = self.client.post(
            login_url,
            {
                "email_or_phone": "johndoe@mail.com",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid Credentials")

    def test_customer_login_empty(self):
        login_url = reverse('customer_login')
        response = self.client.post(
            login_url,
            {
                "email_or_phone": "",
                "password": "",
            },
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Please provide both email/phone and password")
