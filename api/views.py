from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Project, Task, Comment
from api.serializers import UserSignUpSerializer, UserResponseSerializer, TokenObtainPairSerializer, \
    UserUpdateSerializer, ProjectSerializer, TaskSerializer, CommentSerializer

UserModel = get_user_model()


class UserSignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.pop('password')
            serializer.validated_data.pop('confirm_password')
            user = UserModel.objects.create(**serializer.validated_data)
            user.set_password(password)
            user.is_active = True
            user.save()
            return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    queryset = UserModel.objects.all()


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        project = Project.objects.filter(id=self.kwargs.get('project_id')).first()
        if not project:
            raise NotFound(detail=f"Project with id {self.kwargs.get('task_id')} not found.")
        context.update({
            'project': project
        })
        return context

    def get_queryset(self):
        return super(TaskViewSet, self).get_queryset().filter(project_id=self.kwargs.get('project_id'))


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        task = Task.objects.filter(id=self.kwargs.get('task_id')).first()
        if not task:
            raise NotFound(detail=f"Task with id {self.kwargs.get('task_id')} not found.")
        context.update({
            'task': task
        })
        return context

    def get_queryset(self):
        return super(CommentViewSet, self).get_queryset().filter(task_id=self.kwargs.get('task_id'))
