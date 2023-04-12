from rest_framework.response import Response
from .models import Package
from .serializers import PackageSerializer
from rest_framework.viewsets import ModelViewSet


class PackageDetailViewSet(ModelViewSet):
    serializer_class = PackageSerializer
    queryset = Package.objects.all().order_by("id")
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        package = PackageSerializer()
        return Response(data=package.data, status=200)
