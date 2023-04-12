import requests
from django.db import IntegrityError
from rest_framework.response import Response
from .models import User, Transaction
from .serializers import UserSerializer, TransactionSerializer
from rest_framework.viewsets import ModelViewSet
from random import randint
from django.utils import timezone
from ghasedakpack import Ghasedak
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ast import literal_eval
from rest_framework.throttling import UserRateThrottle
from sentry_sdk import capture_exception

sms_validator = None
phone_number = None
activated = None
forget_password = None


class LoginViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]
    authentication_classes = [SessionAuthentication]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        global phone_number
        global sms_validator
        global activated
        global forget_password
        phone_number = User.objects.filter(phone_number=request.data["phone_number"])

        if phone_number:
            phone_number = request.data["phone_number"]
            message = "حساب کاربری یافت شد"
            explanation = "رمز عبور خود را وارد نمایید"
            find_user = True
            return Response({"message": message, "explanation": explanation, "find_user": find_user}, status=200)

        else:
            sms_validator = randint(100000, 999999)
            print(sms_validator)

            # sms = Ghasedak("5d8a1ba6071c1becd307978667d874162f0b09039c8e5c034db7261f7b2eb6e5")
            # sms.send({
            #     "receptor": request.data["phone_number"],
            #     "linenumber": "30005088",
            #     "message": f"""مجله نابغه
            #     کد تایید:{sms_validator}"""
            # })
            activated = False
            phone_number = request.data["phone_number"]
            forget_password = False

            message = "کد تایید ارسال شد"
            explanation = "حساب کاربری با شماره وارد شده وجود ندارد. برای ساخت یک حساب جدید، کد تایید برای این شماره ارسال گردید"
            find_user = False

            return Response({"message": message, "explanation": explanation, "find_user": find_user}, status=201)


class ValidatorViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]
    authentication_classes = [SessionAuthentication]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        global sms_validator
        global activated
        global phone_number
        if request.data["sms_validator"] == sms_validator and request.data["repeat_code"] is False:
            if activated:
                activated = None
            activated = True
            message = "حساب کاربری فعال شد"
            explanation = "حساب کاربری شما با موفقیت ایجاد شد"
            status = True

            return Response({"message": message, "explanation": explanation, "status": status}, status=200)

        elif request.data["repeat_code"] is True:
            sms_validator = randint(100000, 999999)

            # sms = Ghasedak("5d8a1ba6071c1becd307978667d874162f0b09039c8e5c034db7261f7b2eb6e5")
            # sms.send({
            #     "receptor": phone_number,
            #     "linenumber": "30005088",
            #     "message": f"""مجله نابغه
            #     کد تایید:{sms_validator}"""
            # })
            print(sms_validator)

            message = "کد تایید مجدد ارسال شد"
            explanation = "کد تایید مجدد ارسال شده را وارد نمایید"
            status = False

            return Response({"message": message, "explanation": explanation, "status": status}, status=201)

        else:
            message = "کد تایید وارد شده نادرست است"
            explanation = "کد تایید وارد شده نادرست است. لطفا کد صحیح را وارد نمایید"
            status = False

            return Response({"message": message, "explanation": explanation, "status": status}, status=403)


class NewPasswordViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        global phone_number
        global forget_password
        global activated
        password = request.data["password"]
        try:
            if forget_password is False and activated:
                User.objects.create_user(username=phone_number, password=password,
                                         phone_number=phone_number, credit=0, purchased_magazine=[0])

                message = "حساب کاربری ایجاد شد"
                explanation = "به مجله نابغه خوش آمدید. حساب کاربری شما با موفقیت ایجاد شد"

                return Response({"message": message, "explanation": explanation}, status=200)

            elif not activated:
                message = "خطا"
                explanation = "حساب کاربری فعال نشده است"

                return Response({"message": message, "explanation": explanation}, status=403)

            elif forget_password is True and activated:
                User.objects.get(phone_number=phone_number).set_password(password)
                message = "گذرواژه تغییر یافت"
                explanation = "گذرواژه به‌درستی تغییر یافت"

                return Response({"message": message, "explanation": explanation}, status=200)

            else:

                message = "خطا"
                explanation = "در فرآیند ثبت نام خطایی رخ داده است. لطفا مجدد تلاش کنید"

                return Response({"message": message, "explanation": explanation}, status=404)
        except Exception as exception:
            capture_exception(exception)


class PasswordViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        password = request.data["password"]
        global phone_number
        global forget_password
        global sms_validator
        global activated
        if request.data["forget_password"] is True:

            forget_password = True
            new_sms_validator = randint(100000, 999999)

            # sms = Ghasedak("5d8a1ba6071c1becd307978667d874162f0b09039c8e5c034db7261f7b2eb6e5")
            # sms.send({
            #     "receptor": phone_number,
            #     "linenumber": "30005088",
            #     "message": f"""مجله نابغه
            #     کد تایید:{new_sms_validator}"""
            # })

            sms_validator = new_sms_validator
            print(sms_validator)

            activated = False
            message = "کد تایید ارسال شد"
            explanation = "جهت بازیابی گذرواژه، کد تایید ارسال شده را وارد نمایید"

            return Response({"message": message, "explanation": explanation}, status=201)

        else:
            username = User.objects.get(phone_number=phone_number)
            try:

                r = requests.post(url="http://localhost:8000/accounts/api/token/",
                                  data={"username": username.username, "password": password})
                user_token = literal_eval(r.content.decode())
                username.last_login = timezone.now()
                username.save()

                return Response(user_token)
            except Exception as exception:
                capture_exception(exception)


class DashboardViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["post", "get"]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        user_serializer = UserSerializer(instance=user)
        return Response(data=user_serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(username=request.user.username)

            user.update(username=request.data["username"],
                        address=request.data["address"],
                        birth_date=request.data["birth_date"],
                        bio=request.data["bio"],
                        first_name=request.data["first_name"],
                        last_name=request.data["last_name"],
                        email=request.data["email"])

            message = "تغییرات اعمال شد"
            explanation = "اطلاعات کاربری شما به درستی تغییر یافت"

            return Response({"message": message, "explanation": explanation}, status=204)

        except IntegrityError:
            message = "نام کاربری تکراری"
            explanation = "نام کاربری وارد شده تکراری است، لطفا نام کاربری دیگری انتخاب کنید"

            return Response({"message": message, "explanation": explanation}, status=400)

        except Exception as exception:
            capture_exception(exception)


class LogoutViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        try:
            refresh = request.data["refresh"]
            requests.post(url="http://localhost:8000/accounts/api/token/refresh/", data=refresh)

            return Response(data="Logged out", status=205)

        except Exception as exception:
            capture_exception(exception)


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by("payment_date")

    def retrieve(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)
            transaction = Transaction.objects.filter(user=user)
            if transaction:
                transaction_serializer = TransactionSerializer(instance=transaction)
                return Response(data=transaction_serializer.data, status=200)

            else:
                message = "تراکنش ناموجود"
                explanation = "تراکنشی تاکنون صورت نگرفته است"

                return Response({"message": message, "explanation": explanation}, status=400)
        except Exception as exception:
            capture_exception(exception)
