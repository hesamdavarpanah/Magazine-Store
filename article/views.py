from rest_framework.response import Response
from accounts.models import User
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from sentry_sdk import capture_exception

article_id = None


class MainArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by('publish_date')
    http_method_names = ["get"]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by("publish_date")
        article_serializer = ArticleSerializer(instance=articles)
        return Response(data=article_serializer.data, status=200)


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        global article_id
        article_id = int(self.kwargs["id"])
        article = Article.objects.get(id=article_id)
        serializer = ArticleSerializer(article)
        return Response(data=serializer.data, status=200)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ["post", "put", "delete"]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        global article_id
        article = Article.objects.get(id=article_id)
        try:
            Comment.objects.create(username=request.user.username,
                                   user_profile_picture=request.user.profile_picture,
                                   body=request.data["body"],
                                   rate=int(request.data["rate"]),
                                   article=article)

            point = User.objects.get(username=request.user.username)
            point.point += 1
            point.save()

            message = "پیام ثبت شد"
            explanation = "پیام شما با موفقیت ثبت گردید. شما از اشتراک این نظر خود با ما، ۱ امتیاز دریافت کردید"

            return Response({"message": message, "explanation": explanation}, status=201)

        except Exception as exception:
            capture_exception(exception)

    def update(self, request, *args, **kwargs):
        global article_id
        pk = int(self.kwargs["pk"])
        try:
            article = Article.objects.get(id=article_id)
            comment = Comment.objects.get(pk=pk, article=article, username=request.user.username,
                                          user_profile_picture=request.user.profile_picture)

            comment.rate = int(request.data["rate"])
            comment.body = request.data["body"]
            comment.save()

            message = "پیام بروز شد"
            explanation = "پیام شما با موفقیت بروزرسانی شد"

            return Response({"message": message, "explanation": explanation}, status=204)

        except Exception as exception:
            capture_exception(exception)

    def destroy(self, request, *args, **kwargs):
        global article_id
        pk = int(self.kwargs["pk"])
        try:
            article = Article.objects.get(id=article_id)
            comment = Comment.objects.get(pk=pk, article=article, username=request.user.username,
                                          user_profile_picture=request.user.profile_picture)

            comment.delete()

            message = "پیام حذف شد"
            explanation = "پیام شما با موفقیت حذف گردید"

            return Response({"message": message, "explanation": explanation}, status=204)
        except Exception as exception:
            capture_exception(exception)


class SearchViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        articles = Article.objects.filter(body__search=request.data["search"])
        article_serializer = ArticleSerializer(instance=articles, many=True)
        return Response(data=article_serializer.data, status=200)
