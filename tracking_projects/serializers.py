from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import get_user_model
from tracking_projects.models import Project, Contributor
from tracking_projects.models import Issue, Comment

User = get_user_model()


##########################################################################
#                            Serializers Comments
##########################################################################

class CommentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['uuid', 'description', 'author', 'author_name', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    issue_title = serializers.CharField(source='issue.title', read_only=True)
    issue_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'uuid', 'description', 'issue_url', 'issue', 'issue_title',
            'author', 'author_name', 'created_at'
        ]

    def get_issue_url(self, obj):
        """Return the URL to the parent issue"""
        # TODO url Issue
        request = self.context.get('request')
        url = reverse('projects-issues-detail', kwargs={
            'project_pk': obj.issue.project.id,
            'pk': obj.issue.id
        })
        if request:
            return request.build_absolute_uri(url)
        return url

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'description',
        ]


##########################################################################
#                            Serializers Issues
##########################################################################
class IssueDetailSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True, read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    assigned_to_name = serializers.CharField(
        source='assigned_to.username',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'project', 'project_name',
            'author', 'author_name', 'assigned_to', 'assigned_to_name',
            'priority', 'tag', 'status', 'comments', 'created_at'
        ]


class IssueListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'project', 'status', 'priority', 'tag',
            'author', 'author_name', 'assigned_to', 'comments_count'
        ]


class CreateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'title', 'description', 'assigned_to',
            'status', 'priority', 'tag'
        ]

    def validate_assigned_to(self, value):
        """Validate that assigned user is a contributor of the project"""
        if value:
            project = self.context.get('project')
            if project and not Contributor.objects.filter(
                    project=project,
                    user=value
            ).exists():
                raise serializers.ValidationError(
                    "L'utilisateur assigné doit être un contributeur du projet."
                )
        return value


##########################################################################
#                            Serializers Contributors
##########################################################################
class ContributorDetailSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'id', 'user', 'username', 'email',
            'project', 'project_name', 'created_at'
        ]


class ContributorListSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'username', 'email', 'created_at']


class CreateContributorSerializer(Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Cet utilisateur n'existe pas.")
        return value

    def validate(self, attrs):
        project = self.context.get('project')
        user_id = attrs.get('user_id')

        if Contributor.objects.filter(project=project, user=user_id).exists():
            raise serializers.ValidationError(
                "Cet utilisateur est déjà contributeur de ce projet."
            )
        return attrs

    def save(self, **kwargs):
        project = self.context.get('project')
        user_id = self.validated_data['user_id']

        user = User.objects.get(id=user_id)

        contributor = Contributor.objects.create(
            project=project,
            user=user,
        )
        return contributor


##########################################################################
#                            Serializers Projects
##########################################################################
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
        read_only_fields = ['id', 'author', 'contributors', 'issues', 'created_at']


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
        read_only_fields = ['id', 'contributors_count', 'issues_count', 'created_at']

    def get_contributors_count(self, obj):
        """ Return number of contributors """
        return obj.contributors.count()

    def get_issues_count(self, obj):
        """ Return number of issues """
        return obj.issues.count()


class CreateProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'type',
        ]
