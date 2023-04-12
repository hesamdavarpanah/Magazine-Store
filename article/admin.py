from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    pass


class ArticleCommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, ArticleCommentAdmin)
