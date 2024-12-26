from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserSignUpViewSet, CustomTokenObtainPairView, UserViewSet, ProjectViewSet, TaskViewSet

urlpatterns = [
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

router = DefaultRouter(trailing_slash=False)
router.register('users/', UserViewSet, 'user_view')
router.register('users/register/', UserSignUpViewSet, 'user_register')
router.register('projects/', ProjectViewSet, 'projects')
router.register(r'projects/(?P<project_id>\d+)/tasks', TaskViewSet, 'tasks')

urlpatterns += router.urls
