from django.urls import path, include
from rest_framework_nested import routers

from projects.views import ProjectViewset, ContributorViewset

app_name = 'projects'

router = routers.DefaultRouter()
router.register('projects', ProjectViewset, basename='projects')

contributors_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
contributors_router.register('contributors', ContributorViewset, basename='project-contributors')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(contributors_router.urls)),
]
