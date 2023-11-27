import datetime
import uuid

import rstr as rstr
from dateutil.relativedelta import relativedelta
from pytz import timezone, utc

from django.http import JsonResponse
from django.db import transaction

from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, throttle_classes
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config import settings
from weapon.core.utils import make_error_message
from weapon.core.permissions import IsOwnerOrReadOnly, IsPhoneNumberVerifiedOrReadOnly

from .models import PhoneNumber, Profile, RequestDeleteUser, RecommendUser
from .serializers import PhoneNumberSerializer, PhoneNumberVerifySerializer, ProfileSerializer, \
    RequestDeleteUserSerializer, RecommendUserSerializer
from .throttle import PhoneNumberSendRateThrottle
# from ..membership.models import UserMembership
# from ..membership.serializers import UserMembershipSerializer
from ..membership.models import UserMembership
from ..membership.serializers import UserMembershipSerializer
from ..users.views import User

UTC = timezone("UTC")
KST = timezone('Asia/Seoul')


# TODO need to show something...
def confirm_email_success(request):
    return JsonResponse({"status": "allgood"})


def set_recommed_code(profile):
    code = rstr.xeger(r'[A-Z0-9]{5}')
    before_code = Profile.objects.filter(recommend_code=code).first()
    if before_code:
        set_recommed_code(profile)

    profile.recommend_code = code
    profile.save()


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                     mixins.CreateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly, IsPhoneNumberVerifiedOrReadOnly)

    def retrieve(self, request, pk=None):
        if pk == "me":
            if not request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            instance = request.user.profile
        else:
            instance = self.get_queryset().get(pk=pk)
            if not instance.is_teacher:
                return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        if not request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if pk != "me":
            return Response(status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PhoneNumberViewSet(viewsets.GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.CreateModelMixin):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

    @throttle_classes([PhoneNumberSendRateThrottle])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data.get('user')
        phone_number = serializer.validated_data.get('phone_number')
        instance = self.queryset.filter(phone_number=phone_number).first()
        if not instance:
            self.perform_create(serializer)
            instance = self.queryset.filter(phone_number=phone_number).first()

        now = datetime.datetime.utcnow()
        now += datetime.timedelta(minutes=-3)  # 3분안에 보낸 것

        if instance.user != self.request.user:
            instance.is_verified = False

        instance.code = 0
        instance.save()

        # with transaction.atomic():
        #     instance.send_sms()  # 생성된 같은 코드 재발송

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=False, serializer_class=PhoneNumberVerifySerializer)
    def verify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_by_phone_number = serializer.validated_data.get('code_by_phone_number')
        phone_number = serializer.validated_data.get('phone_number')
        instance = self.queryset.filter(phone_number=phone_number).first()

        # phone number not registered
        if not instance:
            return Response(
                make_error_message(100000),
                status=status.HTTP_404_NOT_FOUND)

        # verification failed
        if instance.code != int(code_by_phone_number):
            return Response(
                make_error_message(100001),
                status=status.HTTP_400_BAD_REQUEST)

        instance.is_verified = True

        # 자신의 정보 수정에서 휴대폰 번호 인증완료시에 유저 아이디 추가
        if request.user and request.user.id:
            before_instance = self.queryset.filter(user=request.user).first()
            if before_instance:
                before_instance.delete()

            instance.user = request.user

        instance.save()

        return Response(
            PhoneNumberSerializer(instance).data,
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, throttle_classes=[PhoneNumberSendRateThrottle])
    def resend(self, request):
        phone_number = self.request.data.get('phone_number')
        instance = self.queryset.filter(phone_number=phone_number).first()

        # phone number not registered
        if not instance:
            return Response(
                make_error_message(100000),
                status=status.HTTP_404_NOT_FOUND)

        # To re-generate code
        instance.code = 0
        instance.save()

        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_200_OK)

    @action(detail=False)
    def me(self, request):
        instance = self.queryset.filter(user=self.request.user).first()
        # Not Found

        if not instance:
            return Response(
                make_error_message(100000),
                status=status.HTTP_404_NOT_FOUND)

        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_200_OK)

    def throttled(self, request, wait):
        raise Throttled(detail={
            "message": f"인증번호 발송에 제한되었습니다. {int(wait)}초 후에 가능합니다.",
        })


class CustomUserDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    # user, profile, phone_number 불어오기
    def get(self, *args, **kwargs):
        data = self.get_user_info()
        return Response(data, status.HTTP_200_OK)

    # user, profile, phone_number 수정하기
    def patch(self, request):
        user = self.request.user
        profile = self.request.user.profile

        name = request.data.get('name', None)
        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)
        company = request.data.get('company', None)

        if email:
            user.email = email
            user.save()

        if phone_number:
            profile.phone_number = phone_number

        if company:
            profile.company = company

        if name:
            user.username = name
            user.save()

        profile.is_first_visit = False
        profile.save()

        data = self.get_user_info()
        return Response(data, status.HTTP_200_OK)

    # user, profile, phone_number, interest 불러오는 함수
    def get_user_info(self):
        user = self.request.user

        if user.profile.recommend_code == '':
            set_recommed_code(user.profile)

        s = ProfileSerializer(instance=user.profile)

        data = s.data
        data['id'] = user.id
        data['key'] = user.auth_token.key

        # try:
        #     phone_number_obj = PhoneNumber.objects.get(user=self.request.user, is_verified=True)
        #     data['phone_number'] = phone_number_obj.phone_number
        # except:
        #     data['phone_number'] = None

        data['user_membership'] = None
        now = datetime.datetime.now()
        user_membership = user.user_memberships.filter(is_churned=False, expiry_at__gte=now).order_by(
            '-created_at').first()
        if user_membership:
            data['user_membership'] = UserMembershipSerializer(user_membership).data
        else:
            data['remain_add_user_count'] = 0
            remain_add_user_count = 10 - len(user.customers.all())
            if remain_add_user_count > 0:
                data['remain_add_user_count'] = remain_add_user_count

        return data


class KakaoLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email', None)
        if not email:
            return Response('email error', status=status.HTTP_400_BAD_REQUEST)

        nickname = self.request.data.get('nickname', None)
        thumbnail_image = self.request.data.get('thumbnail_image', "")

        user = User.objects.filter(kakao_email=email).first()
        if not user:
            password = str(uuid.uuid4())
            with transaction.atomic():
                user = User.objects.create(username=nickname, email=email, kakao_email=email, password=password)
                profile = Profile.objects.get(user=user)
                profile.is_kakao = True
                profile.kakao_thumbnail = thumbnail_image
                profile.save()

        profile = Profile.objects.get(user=user)
        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)

        s = ProfileSerializer(instance=profile)
        data = s.data
        data['key'] = str(token)
        data['id'] = user.id

        if profile.recommend_code == '':
            set_recommed_code(user.profile)

        # try:
        #     phone_number_obj = PhoneNumber.objects.get(user=user, is_verified=True)
        #     data['phone_number'] = phone_number_obj.phone_number
        # except:
        #     data['phone_number'] = None

        # is_membership = UserMembership.objects.filter(user=user, is_churned=False, expiry_at__gte=now).order_by(
        #     '-created_at').first()
        #

        data['user_membership'] = None

        now = datetime.datetime.now()
        user_membership = user.user_memberships.filter(is_churned=False, expiry_at__gte=now).order_by(
            '-created_at').first()

        if user_membership:
            data['user_membership'] = UserMembershipSerializer(user_membership).data
        else:
            data['remain_add_user_count'] = 0
            remain_add_user_count = 10 - len(user.customers.filter(is_agree_term=True))
            if remain_add_user_count > 0:
                data['remain_add_user_count'] = remain_add_user_count

        return JsonResponse(data, status=status.HTTP_200_OK)


class RequestDeleteUserViewSet(viewsets.ModelViewSet):
    queryset = RequestDeleteUser.objects.all()
    serializer_class = RequestDeleteUserSerializer


class RecommendCodeView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        my_recommend_user = user.recommend_user.all().first()

        if my_recommend_user:
            return Response('이미 추천한 유저가 있습니다.', status=status.HTTP_400_BAD_REQUEST)

        recommend_code = request.query_params['recommend_code']
        recommend_user_profile = Profile.objects.filter(recommend_code=recommend_code).first()
        recommend_user = recommend_user_profile.user

        if not recommend_user_profile:
            return Response(f'추천 코드 {recommend_code} 의 유저가 없습니다.', status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            recommend_user_instance = RecommendUser()
            recommend_user_instance.user = user
            recommend_user_instance.recommend_user = recommend_user
            recommend_user_instance.save()

            now_date = datetime.datetime.now()
            expiry_at = now_date + relativedelta(months=1)

            user_membership = UserMembership()
            user_membership.user = recommend_user
            user_membership.started_at = now_date
            user_membership.expiry_at = expiry_at
            user_membership.is_free = True

            recommend_user_membership = recommend_user.user_memberships.filter(is_churned=False, expiry_at__gte=now_date).order_by(
            '-created_at').first()

            if recommend_user_membership:
                if not recommend_user_membership.is_churned:
                    if recommend_user_membership.expiry_at > now_date.replace(tzinfo=utc):
                        expiry_at = recommend_user_membership.expiry_at + relativedelta(months=1)
                        user_membership.started_at = recommend_user_membership.started_at
                        user_membership.expiry_at = expiry_at
                        user_membership.membership_payment = recommend_user_membership.membership_payment
                        user_membership.recommend_user = user

            user_membership.save()

        data = RecommendUserSerializer(recommend_user_instance).data
        return Response(data)
