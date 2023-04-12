from rest_framework.serializers import ModelSerializer
from .models import Article, Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ArticleSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
