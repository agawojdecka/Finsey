from django.contrib import admin

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email"]


admin.site.register(User, UserAdmin)
