from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Magazine, Page, Comment
from .serializers import PageSerializer, MagazineSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from sentry_sdk import capture_exception
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist


class MagazineViewSet(ModelViewSet):
    serializer_class = MagazineSerializer
    queryset = Magazine.objects.order_by("-publish_date")
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        serializer = MagazineSerializer()
        return Response(data=serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        magazine = Magazine.objects.get(id=int(request.data["id"]))
        if magazine:
            serializer = MagazineSerializer(instance=magazine)
            return Response(data=serializer.data, status=200)
        else:

            message = "مجله یافت نشد"
            explanation = "مجله مورد نظر شما، یافت نشد. لطفا شماره مجله صحیح را وارد نمایید"

            return Response({"message": message, "explanation": explanation}, status=404)


class DownloadViewSet(ModelViewSet):
    serializer_class = MagazineSerializer
    queryset = Magazine.objects.all()
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        magazine_id = request.data["magazine_id"]
        try:
            user = User.objects.get(username=request.user.username)
            magazine = Magazine.objects.get(id=magazine_id)
            if magazine_id in user.purchased_magazine:
                pdf = open(magazine.magazine_pdf_file.name, 'rb')
                return HttpResponse(FileWrapper(pdf), content_type='application/pdf', status=200)

            elif magazine_id not in user.purchased_magazine and user.credit >= magazine.price:
                if 0 in user.purchased_magazine:
                    user.purchased_magazine.remove(0)
                new_credit = user.credit - magazine.price
                user.purchased_magazine.append(magazine_id)
                user.credit = new_credit
                user.point += 3
                user.save()
                pdf = open(magazine.magazine_pdf_file.name, 'rb')
                return HttpResponse(FileWrapper(pdf), content_type='application/pdf', status=201)

            else:
                message = "اعتبار کافی نیست"
                explanation = "اعتبار شما برای مشاهده این شماره مجله کافی نیست لطفا برای مشاهده این شماره مجله، اعتبار خود را افزایش دهید"
                return Response({"message": message, "explanation": explanation}, status=402)

        except Exception as exception:
            capture_exception(exception)


class PageViewSet(ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    http_method_names = ["post", "get", "delete", "put"]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        magazine_id = int(self.kwargs["magazine_id"])
        page_number = int(self.kwargs["page_number"])
        magazine = Magazine.objects.get(id=magazine_id)
        if page_number > 0:
            try:
                Page.objects.get(page_number=page_number, magazine=magazine)
            except ObjectDoesNotExist:
                return Response({"message": "صفحات مجله به اتمام رسیده است", "explanation": "صفحه یافت نشد"},
                                status=200)

        try:
            user = User.objects.get(username=request.user.username)
            if magazine_id in user.purchased_magazine:
                page = Page.objects.get(page_number=page_number, magazine=magazine)
                serializer = PageSerializer(page)
                return Response(data=serializer.data, status=200)

            elif magazine_id not in user.purchased_magazine and user.credit >= magazine.price:
                if 0 in user.purchased_magazine:
                    user.purchased_magazine.remove(0)
                new_credit = user.credit - magazine.price
                user.purchased_magazine.append(magazine_id)
                user.credit = new_credit
                user.point += 3
                user.save()
                page = Page.objects.get(page_number=page_number, magazine_id=magazine_id)
                serializer = PageSerializer(page)
                return Response(data=serializer.data, status=200)

            else:
                message = "اعتبار کافی نیست"
                explanation = "اعتبار شما برای مشاهده این شماره مجله کافی نیست لطفا برای مشاهده این شماره مجله، اعتبار خود را افزایش دهید"
                return Response({"message": message, "explanation": explanation}, status=402)

        except Exception as exception:
            capture_exception(exception)


class CommentViewSet(ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    http_method_names = ["post", "get", "delete", "put"]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        magazine_id = int(self.kwargs["magazine_id"])
        magazine = Magazine.objects.get(id=magazine_id)
        serializer = MagazineSerializer(magazine)
        return Response(data=serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        magazine_id = int(self.kwargs["magazine_id"])
        magazine = Magazine.objects.get(id=magazine_id)
        try:
            user = User.objects.get(username=request.user.username)
            if magazine_id in user.purchased_magazine:
                Comment.objects.create(username=request.user.username, magazine=magazine, rate=request.data["rate"],
                                       user_profile_picture=request.user.profile_picture, body=request.data["body"])

                user.point += 1
                user.save()
                message = "پیام ثبت شد"
                explanation = "پیام شما با موفقیت ثبت گردید. شما از اشتراک این نظر خود با ما، ۱ امتیاز دریافت کردید"

                return Response({"message": message, "explanation": explanation}, status=201)
            else:
                message = "مجله خریداری نشده"
                explanation = "برای نظر گذاشتن ابتدا مجله را خریداری کنید"

                return Response({"message": message, "explanation": explanation}, status=402)

        except Exception as exception:
            capture_exception(exception)

    def update(self, request, *args, **kwargs):
        magazine_id = int(self.kwargs["magazine_id"])
        pk = int(self.kwargs["pk"])

        magazine = Magazine.objects.get(id=magazine_id)
        try:
            try:
                comment = Comment.objects.get(pk=pk, magazine=magazine, username=request.user.username,
                                              user_profile_picture=request.user.profile_picture)
            except ObjectDoesNotExist:
                message = "پیام بروزرسانی نشد"
                explanation = "شما تنها می توانید پیام‌های خود را بروز کنید"
                return Response({"message": message, "explanation": explanation}, status=200)

            comment.body = request.data["body"]
            comment.rate = request.data["rate"]

            comment.save()

            message = "پیام بروز شد"
            explanation = "پیام شما با موفقیت بروزرسانی شد"

            return Response({"message": message, "explanation": explanation}, status=204)

        except Exception as exception:
            capture_exception(exception)

    def destroy(self, request, *args, **kwargs):
        magazine_id = int(self.kwargs["magazine_id"])
        pk = int(self.kwargs["pk"])

        magazine = Magazine.objects.get(id=magazine_id)
        try:
            try:
                comment = Comment.objects.get(pk=pk, magazine=magazine, username=request.user.username,
                                              user_profile_picture=request.user.profile_picture)
            except ObjectDoesNotExist:
                message = "پیام حذف نشد"
                explanation = "شما تنها می توانید پیام‌های خود را حذف کنید"
                return Response({"message": message, "explanation": explanation}, status=200)
            comment.delete()

            message = "پیام حذف شد"
            explanation = "پیام شما با موفقیت حذف گردید"

            return Response({"message": message, "explanation": explanation}, status=204)

        except Exception as exception:
            capture_exception(exception)


class SearchPageViewSet(ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        magazine_id = int(self.kwargs["magazine_id"])
        magazine = Magazine.objects.get(id=magazine_id)
        try:
            user = User.objects.get(username=request.user.username)
            if magazine_id in user.purchased_magazine:
                page = Page.objects.get(magazine=magazine, description__icontains=request.data["search"])
                serializer = PageSerializer(page)
                return Response(data=serializer.data, status=200)

            elif magazine_id not in user.purchased_magazine and user.credit >= magazine.price:
                if 0 in user.purchased_magazine:
                    user.purchased_magazine.remove(0)
                new_credit = user.credit - magazine.price
                user.purchased_magazine.append(magazine_id)
                user.credit = new_credit
                user.point += 3
                user.save()
                page = Page.objects.get(magazine_id=magazine_id, description__icontains=request.data["search"])
                serializer = PageSerializer(page)
                return Response(data=serializer.data, status=200)

            else:
                message = "اعتبار کافی نیست"
                explanation = "اعتبار شما برای مشاهده این شماره مجله کافی نیست لطفا برای مشاهده این شماره مجله، اعتبار خود را افزایش دهید"
                return Response({"message": message, "explanation": explanation}, status=402)

        except Exception as exception:
            capture_exception(exception)
