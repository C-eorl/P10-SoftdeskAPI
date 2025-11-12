from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from tracking.models import Issue
from .models import Project, Contributor

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
        cls.contributor = Contributor.objects.create(user=cls.user, project=cls.project)
        cls.issue = Issue.objects.create(
            title='Test Issue',
            description='Test description',
            priority='LOW',
            tag='BUG',
            status='To Do',
            project=cls.project,
            author=cls.user,
        )
    def test_create_project(self):
        """Test that project model creation works"""
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test description')
        self.assertEqual(self.project.type, 'front-end')
        self.assertEqual(self.project.author, self.user)
        self.assertIsNotNone(self.project.created_at)

    def test_list_project(self):
        """Test that project list works"""
        url = reverse_lazy('projects:projects-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)

        project = data['results'][0]
        self.assertEqual(project['id'], self.project.pk)
        self.assertEqual(project['name'], self.project.name)
        self.assertEqual(project['description'], self.project.description)
        self.assertEqual(project['type'], self.project.type)
        self.assertEqual(project['author_id'], self.project.author.id)
        self.assertEqual(project['contributor_count'], 1)
        self.assertEqual(project['created_at'], self.project.created_at.isoformat().replace('+00:00', 'Z'),)

    def test_detail_project(self):
        """Test that project detail works"""
        url = reverse_lazy('projects:projects-detail', kwargs={'pk': self.project.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data['id'], self.project.pk)
        self.assertEqual(data['name'], self.project.name)
        self.assertEqual(data['description'], self.project.description)
        self.assertEqual(data['type'], self.project.type)
        self.assertEqual(data['author'], self.project.author.username)
        self.assertEqual(data['author_id'], self.project.author.id)
        self.assertEqual(len(data['contributors']),1)

        contributor_data = data['contributors'][0]
        self.assertEqual(contributor_data['id'], self.contributor.pk)
        self.assertEqual(contributor_data['user'], self.contributor.user.id)
        self.assertEqual(contributor_data['project'], self.contributor.project.pk)
        self.assertEqual(contributor_data['created_at'], self.contributor.created_at.isoformat().replace('+00:00', 'Z'),)

        self.assertEqual(data['issues_count'], 1)
        self.assertEqual(data['created_at'], self.project.created_at.isoformat().replace('+00:00', 'Z'), )


