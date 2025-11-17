from django.contrib import admin
from django.contrib.admin import register

from projects.models import Project
from tracking.models import Issue, Comment


@register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Issue admin class"""
    list_display = ('title', 'description', 'project', 'author', 'priority', 'tag', 'created_at', 'status')


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin class"""
    list_display = ('description', 'issue', 'author', 'created_at')