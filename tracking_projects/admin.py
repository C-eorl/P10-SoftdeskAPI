from tracking_projects.models import Issue, Comment
from django.contrib import admin
from django.contrib.admin import register
from tracking_projects.models import Project, Contributor


@register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Issue admin class"""
    list_display = ('title', 'description', 'project', 'author', 'priority', 'tag', 'created_at', 'status')


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin class"""
    list_display = ('description', 'issue', 'author', 'created_at')


@register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin class"""
    list_display = ('name', 'author', 'created_at', 'type')


@register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """Contributor admin class"""
    list_display = ('user', 'project', 'created_at')