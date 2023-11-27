import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import admin, messages

from weapon.membership.models import Membership, UserMembership, MembershipPayment


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    ordering = ['order']
    list_display = ('name', 'order', 'amount', 'month_amount', 'sale_percent', 'period_month', 'updated_at', 'created_at')
    search_fields = ['id', "name"]


@admin.register(MembershipPayment)
class MembershipPaymentAdmin(admin.ModelAdmin):
    def make_is_refund(modeladmin, request, queryset):
        for payment in queryset.all():
            # 나이스 페이먼츠 환불 처리 로직 시작 =>
            if payment.status == MembershipPayment.STATUS_DICT['결제']:
                payment.status = MembershipPayment.STATUS_DICT['환불']
                user_membership = payment.user_membership.filter(user=payment.user).first()
                if user_membership:
                    user_membership.is_churned = True
                    user_membership.save()
                payment.save()
                messages.add_message(request, messages.INFO, 'payment.id : ' + str(payment.pk) + ' __ 환불로 상태변경 완료')
                pass
            else:
                messages.add_message(request, messages.ERROR, 'payment.id : ' + str(payment.pk) + ' __ 결제 상태가 아닙니다.')

    make_is_refund.short_description = "선택한 유저 환불 처리하기"

    def make_is_paid(modeladmin, request, queryset):
        for payment in queryset.all():
            if payment.status == MembershipPayment.STATUS_DICT['대기']:
                payment.status = MembershipPayment.STATUS_DICT['결제']

                now = datetime.datetime.now()

                expiry_at = now + relativedelta(months=payment.membership.period_month)

                user_membership = UserMembership()
                user_membership.user = payment.user
                user_membership.membership_payment = payment
                user_membership.started_at = now
                user_membership.membership = payment.membership
                user_membership.expiry_at = expiry_at
                user_membership.save()
                payment.save()

                messages.add_message(request, messages.INFO, 'payment.id : ' + str(payment.pk) + ' __ 결제로 상태변경 완료')
                pass
            else:
                messages.add_message(request, messages.ERROR, 'payment.id : ' + str(payment.pk) + ' __ 대기 상태가 아닙니다.')

    make_is_paid.short_description = "선택한 유저 결제 처리하기"

    actions = [make_is_paid, make_is_refund]

    raw_id_fields = ['user']
    list_filter = ['status', 'payment_method']
    list_display = ('id', 'payment_username', 'phone_number', 'amount', 'status', 'payment_method', 'created_at', 'updated_at')
    search_fields = ['id', "user__username", "user__email", "membership__name"]

    def email(self, obj):
        if not obj.user:
            return ''
        return obj.user.email


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_filter = ['is_churned', 'expiry_at']
    list_display = ('id', 'is_churned', 'username', 'email', 'membership_payment', 'started_at', 'expiry_at', 'updated_at', 'created_at')
    search_fields = ['id', "user__username", "user__email"]

    def username(self, obj):
        if not obj.user:
            return ''
        return obj.user.username

    def email(self, obj):
        if not obj.user:
            return ''
        return obj.user.email

