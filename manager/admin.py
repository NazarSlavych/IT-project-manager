from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import Worker, Position, TaskType, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    list_filter = UserAdmin.list_filter + ("position",)

    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )

    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("position",)}),)


admin.site.register(Position)
admin.site.register(TaskType)
admin.site.register(Task)