from django.urls import path, include
from .views import PackageDetailViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("packages", PackageDetailViewSet)

urlpatterns = [
    path('', include(router.urls))
]
