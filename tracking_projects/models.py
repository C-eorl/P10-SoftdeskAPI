from django.core.exceptions import ValidationError
from django.db import models
import uuid
from config import settings


class Issue(models.Model):
    """Problem / Task in project"""
    PRIORITY_CHOICES = [
        ('LOW', 'Basse'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Haute'),
    ]
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Fonctionnalité'),
        ('TASK', 'Tâche'),
    ]
    STATUS_CHOICES = [
        ('To Do', 'À faire'),
        ('In Progress', 'En cours'),
        ('Finished', 'Terminé')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        max_length=15,
        default='MEDIUM',
    )
    tag = models.CharField(
        choices=TAG_CHOICES,
        max_length=15,
        default='TASK',
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=15,
        default='To Do',
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='issues',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='issues',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', '-created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"[{self.tag}] {self.title}"

    def clean(self):
        """Validate that assigned_to is a contributor of the project"""
        super().clean()
        if self.assigned_to and self.project_id:
            if not Contributor.objects.filter(
                    project=self.project, user=self.assigned_to
            ).exists():
                raise ValidationError({
                    'assigned_to': 'L\'utilisateur assigné doit être un contributeur du projet.'
                })


class Comment(models.Model):
    """comment in Issue"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
    )
    description = models.TextField()
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['issue', '-created_at']),
        ]

    def __str__(self):
        return f"Comment {self.uuid} sur {self.issue.title}"


class Project(models.Model):
    """Project model."""
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1024)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save project instance. If new instance add author in contributors"""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.add_contributor(self.author)

    def add_contributor(self, user):
        Contributor.objects.get_or_create(project=self, user=user)


class Contributor(models.Model):
    """Contributor model. Connection between user and project. """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributions'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='contributors'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['project', 'user']),
        ]

    def __str__(self):
        return f"{self.user.username} contribue {self.project.name}"
