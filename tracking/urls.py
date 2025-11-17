from django.urls import path, include
from rest_framework_nested import routers
from tracking.views import IssuesViewset, CommentsViewset
from projects.urls import router as project_router

app_name = 'tracking'

issues_router = routers.NestedDefaultRouter(project_router, 'projects', lookup='project')
issues_router.register(r'issues', IssuesViewset, basename='projects-issues')

comments_router = routers.NestedDefaultRouter(issues_router, 'issues', lookup='issue')
comments_router.register(r'comments', CommentsViewset, basename='issues-comments')

urlpatterns = [
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]