from django.contrib import admin

from apps.savings.models import Goal, Saving

admin.site.register(Saving)
admin.site.register(Goal)
