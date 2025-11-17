from rest_framework import serializers

from tracking.models import Issue, Comment


class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = 'id','issue_id', 'description', 'author'


class CommentDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = 'id', 'uuid', 'description', 'issue', 'author', 'created_at'



class IssueDetailSerializer(serializers.ModelSerializer):

    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'project_id',
            'author', 'author_id', 'assigned_to',
            'priority', 'tag', 'status', 'comments', 'created_at'
        ]



class IssueListSerializer(serializers.ModelSerializer):

    comments_count = serializers.SerializerMethodField()
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'project_id', 'status',
            'author_id', 'comments_count', 'created_at'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


