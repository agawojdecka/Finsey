from django.contrib import admin

from apps.transactions.models import Category, PlannedTransaction, Transaction

admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(PlannedTransaction)
