from django.urls import path, include
from .views import PageViewSet, MagazineViewSet, DownloadViewSet, SearchPageViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"(?P<magazine_id>\d+)/(?P<page_number>\d+)", PageViewSet)
router.register(r"(?P<magazine_id>\d+)/search", SearchPageViewSet)
router.register(r"(?P<magazine_id>\d+)/comments", CommentViewSet)
router.register("main", MagazineViewSet)
router.register("download", DownloadViewSet)

urlpatterns = [
    path('', include(router.urls))
]
