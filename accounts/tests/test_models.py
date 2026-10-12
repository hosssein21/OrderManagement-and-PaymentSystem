from django.db import IntegrityError, transaction
from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.role, User.Roles.CUSTOMER)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)

    @transaction.atomic
    def test_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="test@example.com",
                password="testpassword"
            )

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            email="superuser@example.com",
            password="superuserpassword"
        )
        self.assertEqual(superuser.email, "superuser@example.com")
        self.assertTrue(superuser.check_password("superuserpassword"))
        self.assertIsNotNone(superuser.created_at)
        self.assertIsNotNone(superuser.updated_at)