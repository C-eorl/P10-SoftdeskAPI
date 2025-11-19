from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from tracking_projects.models import Project, Contributor, Issue, Comment
from tracking_projects.permissions import IsContributor, IsContributor
from tracking_projects.serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer,
    ContributorDetailSerializer, IssueListSerializer, IssueDetailSerializer,
    CommentListSerializer,CommentDetailSerializer
)


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsContributor]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        """Add project's author to contributor"""
        project = serializer.save(author=self.request.user)
        project.add_contributor(project.author)


class ContributorViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer


    def get_queryset(self):
        """Return contributors to project"""
        projet_id = self.kwargs['project_pk']
        return Contributor.objects.filter(project_id=projet_id)


class IssuesViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor]


    def get_queryset(self):
        projet_id = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=projet_id)


class CommentsViewset(ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id)