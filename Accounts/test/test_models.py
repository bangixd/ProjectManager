from django.forms import ValidationError
from django.test import TestCase
from Accounts.models import User, Profile
from django.db.utils import IntegrityError

class AccountTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number="09351281828", 
                            first_name="F_1",
                            last_name="L_1",
                            role="CEO",
                            email="test@gmail.com",
                        )
        user.set_password("Password@1234")
        user.save()
    def test_is_create(self):
        """
        Test creating a new user and check if the user details are correct.

        **Test Steps:**
        1. Create a user with known details.
        2. Ensure the user’s first name matches the expected value.
        3. Check if the user’s password matches the given password using `check_password`.
        """
        
        user_1 = User.objects.get(phone_number='09351281828')
        self.assertEqual(user_1.first_name, "F_1")
        self.assertTrue(user_1.check_password("Password@1234"))
    
    def test_unique_phone_number(self):
        """
        Test that the phone number field is unique.

        **Test Steps:**
        1. Try to create a new user with the same phone number as an existing user.
        2. Ensure that an `IntegrityError` is raised due to the unique constraint.
        """

        with self.assertRaises(IntegrityError): # validate unique error
            User.objects.create(phone_number="09351281828", 
                                first_name="F_2",
                                last_name="L_2",
                                role="Manager",
                                email="test2@gmail.com",
                                password="abcd1234"
                            )
    
    def test_profile_created_with_user(self):
        """
        Test that a profile is automatically created when a user is created.

        **Test Steps:**
        1. Create a new user.
        2. Ensure that a profile is created for the user.
        3. Check that the profile’s user matches the created user.
        4. Verify that the profile image is set to the default image.
        """
        
        user = User.objects.get(phone_number="09351281828")
        
        self.assertTrue(Profile.objects.filter(user=user).exists())
        
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.user.first_name, user.first_name)
        self.assertEqual(profile.image.name, 'accounts/profile/defualt/default_avatar.jpg')
    
    def test_default_fields(self):
        """
        Test the default values of the user model fields.

        **Test Steps:**
        1. Create a new user.
        2. Verify the default values of `is_active`, `is_staff`, `is_superuser`, and `is_vip` fields.
        """
        
        user = User.objects.get(phone_number="09351281828")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_vip)
    
    def test_change_password(self):
        """
        Test changing the user's password.

        **Test Steps:**
        1. Retrieve an existing user.
        2. Change the user's password using `set_password`.
        3. Ensure the password is successfully updated by verifying with `check_password`.
        """

        user = User.objects.get(phone_number="09351281828")

        user.set_password("NewPassword@1234")
        user.save()
        self.assertTrue(user.check_password("NewPassword@1234"))

    def test_invalid_phone_number(self):
        """
        Test the validation of the phone number field.

        **Test Steps:**
        1. Attempt to create a user with an invalid phone number format.
        2. Ensure that a `ValidationError` is raised due to the invalid phone number.
        """
        
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                phone_number="12345",
                first_name="Invalid",
                last_name="User",
                role="Manager",
                email="invalid.user@example.com",
                password="Invalid@123"
            )
    
    def test_user_profile_deletion(self):
        """
        Test that the user’s profile is deleted when the user is deleted.

        **Test Steps:**
        1. Create a user.
        2. Delete the user.
        3. Ensure that the associated profile is also deleted.
        """
        
        user = User.objects.get(phone_number="09351281828")
        user_id = user.id
        user.delete()
        self.assertFalse(Profile.objects.filter(user_id=user_id).exists())
        
    def test_create_superuser(self):
        """
        Test creating a superuser.

        **Test Steps:**
        1. Create a superuser using `create_superuser`.
        2. Verify that the superuser has `is_staff` and `is_superuser` set to `True`.
        """
        
        superuser = User.objects.create_superuser(
            phone_number="09987654321",
            first_name="Admin",
            last_name="User",
            role="CEO",
            email="admin@example.com",
            password="Admin@1234"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)