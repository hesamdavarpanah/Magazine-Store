from django.urls import path, include
from .views import ContactUsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", ContactUsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
