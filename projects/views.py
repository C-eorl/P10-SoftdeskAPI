from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from projects.models import Project, Contributor
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, \
    ContributorDetailSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()


class ContributorViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer


    def get_queryset(self):
        projet_id = self.kwargs['project_pk']
        return Contributor.objects.filter(project_id=projet_id)
