from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor


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
    author  =serializers.StringRelatedField(read_only=True)
    contributors = ContributorListSerializer(many=True, read_only=True)
    issues_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'type',
            'author', 'contributors', 'issues_count', 'created_at'
        ]

    def get_issues_count(self, obj):
        """ Return number of issues """
        return obj.issues.count()


class ProjectListSerializer(ModelSerializer):
    """ Serializer for Project objects (list & create)"""
    contributor_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'type', 'author_id',
            'contributor_count', 'created_at',
        ]

    def get_contributor_count(self, obj):
        """ Return number of contributors """
        return obj.contributors.count()