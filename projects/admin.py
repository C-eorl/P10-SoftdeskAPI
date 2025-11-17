from django.contrib import admin
from django.contrib.admin import register

from projects.models import Project, Contributor


@register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin class"""
    list_display = ('name', 'author', 'created_at', 'type')


@register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """Contributor admin class"""
    list_display = ('user', 'project', 'created_at')