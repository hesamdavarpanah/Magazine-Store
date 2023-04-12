from rest_framework.serializers import ModelSerializer
from .models import Magazine, Page, Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PageSerializer(ModelSerializer):

    class Meta:
        model = Page
        fields = ["title", "description", "publish_date", "image", "magazine"]


class MagazineSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Magazine
        fields = ["id", "title", "description", "publish_date", "price", "cover_image", "comments"]
