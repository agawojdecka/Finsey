from django.contrib import admin

from apps.savings.models import Saving, Purpose


admin.site.register(Saving)
admin.site.register(Purpose)
