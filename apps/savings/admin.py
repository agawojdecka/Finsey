from django.contrib import admin

from apps.savings.models import Saving, Purpose, Goal


admin.site.register(Saving)
admin.site.register(Purpose)
admin.site.register(Goal)
