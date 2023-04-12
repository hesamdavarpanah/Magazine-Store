from django.urls import path, include
from .views import ValidatorViewSet, LoginViewSet, TransactionViewSet, DashboardViewSet, NewPasswordViewSet, \
    PasswordViewSet, LogoutViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()

router.register("login", LoginViewSet)
router.register("validator", ValidatorViewSet)
router.register("new-password", NewPasswordViewSet)
router.register("password", PasswordViewSet)
router.register("dashboard", DashboardViewSet)
router.register("transaction", TransactionViewSet, basename="Transaction")
router.register("logout", LogoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view()),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view()),
]
