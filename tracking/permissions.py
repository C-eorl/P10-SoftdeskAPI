from rest_framework import permissions

from projects.models import Project


class IsTrackingContributor(permissions.BasePermission):
    """Permission to check if a user is project contributor """
    message = "Vous devez être contributeur du projet pour accéder à cette issue/comments"
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
        else:
            return False
        return project.contributors.filter(user=request.user).exists()
