from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    pass


admin.site.register(ContactUs, ContactUsAdmin)
