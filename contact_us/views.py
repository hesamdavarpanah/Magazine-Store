from rest_framework.response import Response
from .models import ContactUs
from .serializers import ContactUsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import UserRateThrottle


class ContactUsViewSet(ModelViewSet):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    http_method_names = ["post"]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        contact_us = ContactUs.objects.filter(phone_number=request.data["phone_number"],
                                              body=request.data["body"])

        if contact_us:
            message = "پیام شما قبلا ثبت شده است"
            explanation = "پیام شما قبلا ثبت شده است لطفا منتظر تماس همکاران ما باشید از شکیبایی شما سپاسگزاریم"
            return Response({"message": message, "explanation": explanation}, status=409)

        else:
            ContactUs.objects.create(phone_number=request.data["phone_number"],
                                     body=request.data["body"])

            message = "پیام شما با موفقیت ثبت شد"
            explanation = "پیام شما با موفقیت ثبت شد. به‌زودی همکاران ما با شما تماس خواهند گرفت"
            return Response({"message": message, "explanation": explanation}, status=201)
