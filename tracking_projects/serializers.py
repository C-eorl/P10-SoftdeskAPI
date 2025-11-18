from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from tracking_projects.models import Project, Contributor
from tracking_projects.models import Issue, Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'id', 'issue_id', 'description', 'author'


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


class ContributorDetailSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class ContributorListSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = 'id', 'username'

    def get_username(self, obj):
        return obj.user.username


class ProjectDetailSerializer(ModelSerializer):
    """ Serializer for project detail """
    author = serializers.StringRelatedField(read_only=True)
    contributors = ContributorListSerializer(many=True, read_only=True)
    issues = IssueListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'type',
            'author', 'contributors', 'issues', 'created_at'
        ]


class ProjectListSerializer(ModelSerializer):
    """ Serializer for Project objects (list & create)"""
    contributors_count = serializers.SerializerMethodField()
    issues_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'type',
            'contributors_count', 'issues_count', 'created_at',
        ]

    def get_contributors_count(self, obj):
        """ Return number of contributors """
        return obj.contributors.count()

    def get_issues_count(self, obj):
        """ Return number of issues """
        return obj.issues.count()
