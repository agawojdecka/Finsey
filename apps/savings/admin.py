from django.contrib import admin

from apps.savings.models import Saving, Goal


admin.site.register(Saving)
admin.site.register(Goal)
