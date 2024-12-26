from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserSignUpViewSet, CustomTokenObtainPairView

urlpatterns = [
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

router = DefaultRouter(trailing_slash=False)
router.register('users/register/', UserSignUpViewSet, 'user_register')

urlpatterns += router.urls
