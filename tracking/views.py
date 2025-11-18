from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from tracking.models import Issue, Comment
from tracking.permissions import IsTrackingContributor
from tracking.serializers import IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer


class IssuesViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsTrackingContributor]


    def get_queryset(self):
        projet_id = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=projet_id)


class CommentsViewset(ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsTrackingContributor]

    def get_queryset(self):
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id)

