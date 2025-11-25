from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from tracking_projects.models import Project, Contributor, Issue, Comment
from tracking_projects.permissions import IsContributor, IsAuthor
from tracking_projects.serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer,
    ContributorDetailSerializer, IssueListSerializer, IssueDetailSerializer,
    CommentListSerializer, CommentDetailSerializer, CreateContributorSerializer, CreateIssueSerializer,
    CreateCommentSerializer, CreateProjectSerializer
)


class ProjectViewset(ModelViewSet):
    """
    ViewSet for Project.

    [Permission]
    - List/Retrieve: Any authenticated contributor
    - Create: Any authenticated user (auto-added as contributor)
    - Update/Delete: Only project author

    [Endpoint]
    - List : GET /api/v1/projects/
    - Retrieve: GET /api/v1/projects/<int:project_id>
    - Create: POST /api/v1/projects/
    - Update: PUT/PATCH /api/v1/projects/<int:project_id>
    - Delete: DELETE /api/v1/projects/<int:project_id>
    """

    def get_queryset(self):
        """Return projects where user is a contributor"""
        user = self.request.user
        return Project.objects.filter(contributors__user=user).distinct()

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsContributor()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CreateProjectSerializer
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        """Save project with current user as author"""
        serializer.save(author=self.request.user)


class ContributorViewset(ModelViewSet):
    """
    ViewSet for Contributor management.

    [Permission]
    - List/Retrieve: Any contributor of the project
    - Create/Update/Delete: Only project author

    [Endpoint]
    - List: GET /api/v1/projects/<int:project_id>/contributors/
    - Retrieve: GET /api/v1/projects/<int:project_id>/contributors/<int:contributor_id>
    - Create: POST /api/v1/projects/<int:project_id>/contributors/
    - Update: PUT/PATCH /api/v1/projects/<int:project_id>/contributors/<int:contributor_id>
    - Delete: DELETE /api/v1/projects/<int:project_id>/contributors/<int:contributor_id>
    """

    def get_queryset(self):
        """Return contributors to specified project"""
        projet_id = self.kwargs['project_pk']
        return Contributor.objects.filter(project_id=projet_id)

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsContributor()]
        if self.action in ['destroy', 'update', 'partial_update', 'create']:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ContributorDetailSerializer
        if self.action == 'list':
            return ContributorListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CreateContributorSerializer
        return ContributorListSerializer

    def get_serializer_context(self):
        """Add project to serializer context for create action"""
        context = super().get_serializer_context()
        if self.action == 'create':
            project_id = self.kwargs['project_pk']
            context['project'] = get_object_or_404(Project, id=project_id)
        return context


class IssuesViewset(ModelViewSet):
    """
    ViewSet for Issue.

    [Permission]
    - List/Retrieve/Create: Any contributor of the project
    - Update/Delete: Only issue author

    [Endpoint]
    - List: GET /api/v1/projects/<int:project_id>/issues/
    - Retrieve: GET /api/v1/projects/<int:project_id>/issues/<int:issue_id>
    - Create: POST /api/v1/projects/<int:project_id>/issues/
    - Update: PUT/PATCH /api/v1/projects/<int:project_id>/issues/<int:issue_id>
    - Delete: DELETE /api/v1/projects/<int:project_id>/issues/<int:issue_id>
    """

    def get_queryset(self):
        """Return issues for the specified project"""
        projet_id = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=projet_id)

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated(), IsContributor()]
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated(), IsContributor()]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateIssueSerializer
        if self.action == 'list':
            return IssueListSerializer
        if self.action == 'retrieve':
            return IssueDetailSerializer
        return IssueListSerializer

    def get_serializer_context(self):
        """Add project to serializer context"""
        context = super().get_serializer_context()
        project_id = self.kwargs.get('project_pk')
        context['project'] = get_object_or_404(Project, id=project_id)
        return context

    def perform_create(self, serializer):
        """Save issue with current user as author and link to project"""
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project, author=self.request.user)


class CommentsViewset(ModelViewSet):
    """
    ViewSet for Comment.

    [Permission]
    - List/Retrieve/Create: Any contributor of the project
    - Update/Delete: Only comment author

    [Endpoint]
    - List: GET /api/v1/projects/<int:project_id>/issues/<int:issue_id>/comments/
    - Retrieve: GET /api/v1/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>
    - Create: POST /api/v1/projects/<int:project_id>/issues/<int:issue_id>/comments/
    - Update: PUT/PATCH /api/v1/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>
    - Delete: DELETE /api/v1/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>
    """

    def get_queryset(self):
        """Return comments for the specified issue"""
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id)

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated(), IsContributor()]
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated(), IsContributor()]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateCommentSerializer
        if self.action == 'list':
            return CommentListSerializer
        if self.action == 'retrieve':
            return CommentDetailSerializer
        return CommentListSerializer

    def perform_create(self, serializer):
        """Save comment with current user as author and link to issue"""
        issue_id = self.kwargs.get('issue_pk')
        issue = get_object_or_404(Issue, id=issue_id)
        serializer.save(author=self.request.user, issue=issue)
