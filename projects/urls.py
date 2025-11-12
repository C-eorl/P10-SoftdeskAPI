from django.urls import path, include
from rest_framework import routers

from projects.views import ProjectViewset, ContributorViewset

app_name = 'projects'

router = routers.SimpleRouter()

router.register('projects', ProjectViewset, basename='projects')
router.register('contributors', ContributorViewset, basename='contributors')

urlpatterns = [
    path('', include(router.urls))
]
