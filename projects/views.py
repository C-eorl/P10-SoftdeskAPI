from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from projects.models import Project, Contributor
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, \
    ContributorDetailSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

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
