from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Project

User = get_user_model()

class ProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Initialize data for test"""
        cls.user = User.objects.create_user(
            username="testuser",
            password="password",
            age=22
        )
        cls.project = Project.objects.create(
            name='Test Project',
            description='Test description',
            type='front-end',
            author=cls.user,
        )

    def test_create_project(self):
        """Test that project creation works"""
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test description')
        self.assertEqual(self.project.type, 'front-end')
        self.assertEqual(self.project.author, self.user)
        self.assertIsNotNone(self.project.created_at)
