from django.urls import path, include
from rest_framework_nested import routers
from tracking_projects.views import IssuesViewset, CommentsViewset
from tracking_projects.views import ProjectViewset, ContributorViewset

app_name = 'tracking_project'

router = routers.DefaultRouter()
router.register('projects', ProjectViewset, basename='projects')

contributors_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
contributors_router.register('contributors', ContributorViewset, basename='project-contributors')

issues_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
issues_router.register(r'issues', IssuesViewset, basename='projects-issues')

comments_router = routers.NestedDefaultRouter(issues_router, 'issues', lookup='issue')
comments_router.register(r'comments', CommentsViewset, basename='projects-issues-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(contributors_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]
