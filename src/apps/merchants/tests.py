from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.merchants.models import Merchant, MerchantProfile


class MerchantSignupTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('merchants_signup')

    def test_merchant_signup_success(self):
        data = {
            "business_name": "John Doe",
            "email": "johndoe@mail.com",
            "password": "passwordMm-123456",
            "phone_number": "12345678901",
            "address": "1234 Main St",
            "payment_information": "Cash",
            "terms_agreement": True,
        }


        response = self.client.post(self.signup_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Merchant.objects.count(), 1)
        self.assertEqual(Merchant.objects.get(email="johndoe@mail.com").full_name, "John Doe")
        self.assertTrue(MerchantProfile.objects.filter(merchant__email="johndoe@mail.com").exists())

    
    def test_merchant_signup_fail(self):
        data = {
            "business_name": "John Doe",
            "email": "johndoe@mail.com",
            "password": "passwordMm",
            "phone_number": "1234567801",
            "address": "1234 Main St",
            "payment_information": "",
            "terms_agreement": True,
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Merchant.objects.count(), 0)
        self.assertEqual(MerchantProfile.objects.count(), 0)


    

class MerchantLoginTest(APITestCase):
    def setUp(self):
        try:
            self.merchant = Merchant.objects.create_merchant(
                email="test@example.com",
                full_name='Test Merchant',
                address="1234 Main St",
                payment_information="Cash",
                terms_agreement=True,
                phone_number="1234567890",
                password="password",
            )
            self.merchant.save()
        except Exception as e:
            print(f"Error creating Merchant in setUp: {e}")

    def test_merchant_profile_creation(self):
        profile_exists = MerchantProfile.objects.filter(merchant=self.merchant).exists()
        self.assertTrue(profile_exists, "MerchantProfile should be created for a new Merchant")

    def test_merchant_login(self):
        login_url = reverse('merchants_login')
        login_data = {
            "email_or_phone": "test@example.com",
            "password": "password",
        }

        response = self.client.post(login_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('merchant', response.data)

