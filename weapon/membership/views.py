from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from pytz import timezone

from weapon.membership.models import MembershipPayment, UserMembership, Membership
from weapon.membership.serializers import MembershipPaymentSerializer, UserMembershipSerializer, MembershipSerializer, \
    UserMembershipSerializerForPayment

UTC = timezone("UTC")


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = MembershipPayment.objects.all()
    serializer_class = MembershipPaymentSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        membership = request.data.get('membership')
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')
        payment_username = request.data.get('payment_username')
        phone_number = request.data.get('phone_number')

        membership_payment = MembershipPayment()
        membership_payment.user_id = user
        membership_payment.membership_id = membership
        membership_payment.amount = amount
        membership_payment.payment_method = int(payment_method)
        if payment_username:
            membership_payment.payment_username = payment_username
        if phone_number:
            membership_payment.phone_number = phone_number

        membership_payment.save()

        data = MembershipPaymentSerializer(membership_payment).data
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user).order_by('-created_at'))

        pages = self.paginate_queryset(queryset)
        id_list = []
        if pages is not None:
            for page in pages:
                id_list.append(page.id)

            serializer = self.get_serializer(pages, many=True)
            data_list = serializer.data

            payment_dict = {}
            for data in data_list:
                payment_dict[data.get('id')] = data

            user_membership_list = UserMembership.objects.filter(membership_payment_id__in=id_list)

            for user_membership in user_membership_list:
                payment_dict[user_membership.membership_payment.id]['user_membership'] = UserMembershipSerializerForPayment(
                    user_membership).data

            return self.get_paginated_response(data_list)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('order')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserMembershipViewSet(viewsets.ModelViewSet):
    queryset = UserMembership.objects.all()
    serializer_class = UserMembershipSerializer

    @action(detail=False)
    def me(self, request):
        user = self.request.user
        instance = UserMembership.objects.filter(user=user).order_by('-created_at')
        serializer = UserMembershipSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def get_refund_amount(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        refund_amount = instance.get_refund_amount()
        remaining_days = instance.get_remaining_days()
        return Response({
            "refund_amount": refund_amount,
            "remaining_days": remaining_days
        }, status=status.HTTP_200_OK)

