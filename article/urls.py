from django.urls import path, include
from .views import MainArticleViewSet, SearchViewSet, ArticleViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("main", MainArticleViewSet)
router.register(r"(?P<id>\d+)", ArticleViewSet)
router.register("search", SearchViewSet)
router.register("comment", CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
