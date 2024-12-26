from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Project(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_owner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    ADMIN, MEMBER = 'Admin', 'Member'
    ROLE_CHOICES = (
        (ADMIN, ADMIN),
        (MEMBER, MEMBER),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_members')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user


class Task(models.Model):
    TODO, PROGRESS, DONE = 'TO Do', 'Progress', 'Done'
    STATUS_CHOICES = (
        (TODO, TODO),
        (PROGRESS, PROGRESS),
        (DONE, DONE)
    )
    LOW, MEDIUM, HIGH = 'Low', 'Medium', 'High'
    PRIORITY_CHOICES = (
        (LOW, LOW),
        (MEDIUM, MEDIUM),
        (HIGH, HIGH)
    )
    title = models.CharField(max_length=500)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    assign_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_tasks', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
