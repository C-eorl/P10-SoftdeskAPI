from rest_framework import permissions

from tracking_projects.models import Project


class IsContributor(permissions.BasePermission):
    """Permission to check if a user is project contributor """
    message = "Vous devez être contributeur du projet pour accéder à l'ensemble di projet"
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        return project.contributors.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        """
        For Issue cas, search Issue.project
        For Comment cas, search Comment.issue.project
        """

        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project
        elif type(obj) is Project:
            project = obj
        else:
            return False
        return project.contributors.filter(user=request.user).exists()


class IsAuthor(permissions.BasePermission):
    """Permission to check if a user is author """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            author = obj.author
        else:
            return False
        return author == request.user