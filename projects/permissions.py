from rest_framework import permissions


class IsProjectContributor(permissions.BasePermission):
    """Permission class to check if a user is contributor to project"""

    message = "Vous devez être contributeur de ce projet pour y accéder."

    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()