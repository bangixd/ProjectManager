from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from Accounts.models import User, Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class AccountTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09351281828",
            first_name="Test",
            last_name="User",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        self.client = APIClient()
        self.login_url = reverse('accounts:user_login')
        self.profile_url = reverse('accounts:user_profile')
        self.logout_url = reverse('accounts:user_logout')
        self.change_password_url = reverse('accounts:user_change_password')
        self.password_reset_request_url = reverse('accounts:password_reset_request')
        
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.password_reset_confirm_url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})
        

    def test_authenticate_user(self):
        """
        Helper method to authenticate user and set token in headers.
        """
        response = self.client.post(self.login_url, {'phone_number': self.user.phone_number, 'password': "Password@1234"})
        # print('Response: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('access')
        # print(f'token is {token}')
        self.assertIsNotNone(token, "Token should not be None") 
        self.access_token = response.data.get('access')
        self.refresh_token = response.data.get('refresh')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_create_user(self):
        """
        Test creating a new user account.
        """
        response = self.client.post(reverse('accounts:create_user'), {
            'phone_number': '09123456789',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'Manager',
            'email': 'newuser@gmail.com',
            'password': 'Password@1234'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(phone_number='09123456789').count(), 1)

    def test_user_profile_detail(self):
        """
        Test retrieving user profile details.
        """
        self.test_authenticate_user()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(f"the response.data['first_name'] => {response.data[0]['first_name']}\nself.user.first_name => {self.user.first_name}")
        self.assertEqual(response.data[0]['first_name'], self.user.first_name)

    def test_user_logout(self):
        """
        Test logging out the authenticated user.
        """
        self.test_authenticate_user() 
        response = self.client.post(self.logout_url, {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_change_password(self):
        """
        Test changing the user's password.
        """
        self.test_authenticate_user()
        response = self.client.put(self.change_password_url, {
            'old_password': 'Password@1234',
            'new_password': 'NewPassword@1234',
            'confirm_password': 'NewPassword@1234'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the user instance from the database
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword@1234'))

    def test_password_reset_request(self):
        """
        Test requesting a password reset.
        """
        self.client.credentials()  # Clear any token if set
        self.assertTrue(User.objects.filter(email=self.user.email).exists())  # Ensure email exists
        response = self.client.post(self.password_reset_request_url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        