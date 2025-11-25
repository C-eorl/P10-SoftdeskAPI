from rest_framework import permissions


from tracking_projects.models import Project, Issue, Comment


class IsContributor(permissions.BasePermission):
    """Permission to check if a user is project contributor """
    message = "Vous devez être contributeur du projet pour accéder à l'ensemble du projet"

    def has_permission(self, request, view):

        if view.kwargs.get('project_pk'):
            project_id = view.kwargs.get('project_pk')
            project = Project.objects.get(pk=project_id)
            return project.contributors.filter(user=request.user).exists()

        if not view.kwargs.get('project_pk'):
            return True

        return False

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

    message = "Vous devez être l'auteur de cette ressource pour modifier / supprimer"

    def has_permission(self, request, view):
        kwargs = view.kwargs

        # Cas Comment
        if all(k in kwargs for k in ["project_pk", "issue_pk", "pk"]):
            comments_pk = view.kwargs.get('pk')
            comments = Comment.objects.get(pk=comments_pk)
            return comments.author == request.user

        # Cas Issue
        if all(k in kwargs for k in ["project_pk", "pk"]):
            issues_pk = view.kwargs.get('pk')
            issues = Issue.objects.get(pk=issues_pk)
            return issues.author == request.user

        # Cas Project
        if "pk" in kwargs:
            project_id = view.kwargs.get('pk')
            project = Project.objects.get(pk=project_id)
            return project.author == request.user
        return False

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            author = obj.author
        elif hasattr(obj, 'project'):
            return obj.project.author == request.user
        else:
            return False
        return author == request.user
