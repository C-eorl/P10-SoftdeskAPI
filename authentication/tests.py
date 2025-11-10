from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
User = get_user_model()

class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_default = User.objects.create_user(
            username="testuser",
            password="password",
            age=25
        )
    def setUp(self):
        self.minor_user = User(
            username="minor",
            password="password",
            age=15
        )

    def test_create_user(self):
        """Test creating a new default user"""
        self.assertEqual(self.user_default.username, "testuser")
        self.assertTrue(self.user_default.check_password("password"))
        self.assertEqual(self.user_default.age, 25)
        self.assertEqual(self.user_default.can_be_contacted, False)
        self.assertEqual(self.user_default.can_data_be_shared, False)
        self.assertIsNotNone(self.user_default.created_at)

    def test_user_consent(self):
        """Test that user consent is correct"""
        self.user_default.can_be_contacted = True
        self.user_default.can_data_be_shared = True

        self.assertEqual(self.user_default.can_be_contacted, True)
        self.assertEqual(self.user_default.can_data_be_shared, True)

    def test_not_create_user_age_inf_fifteen(self):
        """Test creating a new default user with age inf fifteen"""
        with self.assertRaises(ValidationError):
            self.minor_user.full_clean()

