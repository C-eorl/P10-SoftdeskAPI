from rest_framework.viewsets import ReadOnlyModelViewSet

from projects.models import Project, Contributor
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer


class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Project.objects.all()

        type_project = self.request.GET.get('type')
        if type_project is not None:
            queryset = queryset.filter(type=type_project)


        return queryset  # Possibilité de filter .filter()


class ContributorViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()
