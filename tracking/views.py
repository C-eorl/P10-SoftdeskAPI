from rest_framework.viewsets import ReadOnlyModelViewSet

from tracking.models import Issue, Comment
from tracking.serializers import IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer


class IssuesViewset(ReadOnlyModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        projet_id = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=projet_id)


class CommentsViewset(ReadOnlyModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id)

