from django.contrib import admin
from .models import User, Transaction


class UserAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
