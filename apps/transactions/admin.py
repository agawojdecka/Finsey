from django.contrib import admin

from apps.transactions.models import Transaction, Category

admin.site.register(Transaction)
admin.site.register(Category)
