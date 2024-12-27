from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from api.models import Project, Task, Comment, ProjectMember

# Register your models here.
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name',)


class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('ADMIN', 'MEMBER')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'assign_to', 'project', 'due_date')
    list_filter = ('status', 'priority', 'due_date', 'project')
    search_fields = ('title',)


class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role')
    list_filter = ('project', 'role')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'task')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(Comment, CommentAdmin)
