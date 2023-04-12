from django.contrib import admin
from .models import Magazine, Page, Comment


class MagazineAdmin(admin.ModelAdmin):
    pass


class PageAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Magazine, MagazineAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Comment, CommentAdmin)
