from django.contrib import admin

from apps.transactions.models import Category, Transaction

admin.site.register(Transaction)
admin.site.register(Category)
