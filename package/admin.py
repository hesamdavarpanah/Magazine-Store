from django.contrib import admin
from .models import Package


class PackageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Package, PackageAdmin)
