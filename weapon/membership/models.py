import math
from datetime import datetime

from django.db import models
from django.conf import settings


class Membership(models.Model):
    name = models.CharField('멤버십 이름', max_length=100)
    product_amount = models.IntegerField('멤버십 가격', default=0)
    sale_percent = models.SmallIntegerField('세일 퍼센트', default=0)
    period_month = models.SmallIntegerField('멤버십 기간 개월수', default=0)
    order = models.SmallIntegerField('순서 (낮은 순)')
    is_recommend = models.BooleanField('추천 유무', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = '멤버십'
        verbose_name_plural = '멤버십'

    def month_amount(self):
        sale_amount = 0
        if self.sale_percent > 0:
            sale_amount = self.product_amount / 100 * self.sale_percent
        result = self.product_amount - sale_amount
        result = result / self.period_month
        return result

    def amount(self):
        sale_amount = 0
        if self.sale_percent > 0:
            sale_amount = self.product_amount / 100 * self.sale_percent
        result = self.product_amount - sale_amount
        return result


class MembershipPayment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True
    )
    membership = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True
    )
    STATUS = (
        (-1, '대기'),  # 미결제
        (-2, '취소'),  # 결제취소
        (-3, '실패'),  # 결제실패
        (-4, '환불'),  # 환불완료
        (1, '결제'),  # 결제완료
    )

    STATUS_DICT = {v: k for k, v in STATUS}

    METHODS = (  # Iamport 결제 방식 카테고리
        (1, '계좌'),  # 계좌
        (2, '논PG'),  # 논피지
    )

    METHODS_DICT = {v: k for k, v in METHODS}

    amount = models.PositiveIntegerField('결제 가격')
    status = models.SmallIntegerField('결제 상태', choices=STATUS, default=-1)
    # status_message = models.CharField('결제 상태 메시지', max_length=200, blank=True, default='')
    payment_method = models.SmallIntegerField('결제 수단', choices=METHODS, default=1)

    payment_username = models.CharField('임급자명', max_length=10, blank=True, default="")
    phone_number = models.CharField('결제링크수신번호', max_length=15, blank=True, default="")

    # card_number = models.CharField('카드 넘버', max_length=20, blank=True, default='')
    # card_name = models.CharField('카드 이름', max_length=10, blank=True, default='')
    # card_option = models.CharField('', max_length=20, blank=True, default='')
    # merchant_uid = models.CharField(max_length=255, unique=True)
    # pg = models.CharField(max_length=20, blank=True, default="NICE")
    # tid = models.CharField(max_length=100, blank=True, default="")
    # buyer_email = models.EmailField()
    # is_sale = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.id}, amount: {self.amount}"

    class Meta:
        verbose_name = '결제내역'
        verbose_name_plural = '결제내역'

    def cancel(self):
        return True, self


class UserMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_memberships",
    )
    membership_payment = models.ForeignKey(
        MembershipPayment,
        on_delete=models.SET_NULL,
        related_name="user_memberships",
        null=True
    )
    recommend_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recommend_user_memberships",
    )
    started_at = models.DateTimeField('시작일')
    expiry_at = models.DateTimeField('만료일')
    is_free = models.BooleanField('무료유무', default=False)
    is_churned = models.BooleanField('환불유무', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_remaining_days(self):
        # expiry_at = self.expiry_at.replace(tzinfo=None)
        # now = datetime.utcnow()
        # remaining_days = abs(expiry_at - now).days + 1
        # return remaining_days
        return None

    def get_refund_amount(self):
        # start_date_at = self.started_at.replace(tzinfo=None)
        # expiry_at = self.expiry_at.replace(tzinfo=None)
        # remaining_days = self.get_remaining_days()
        # full_days = abs(expiry_at - start_date_at).days
        # percent = remaining_days / full_days * 100
        # excluding_fees_amount = self.membership_payment.amount - (self.membership_payment.amount * 0.03)  # 3 퍼센트 결제 수수료 제외
        # cancel_amount = excluding_fees_amount / 100 * percent
        # cancel_amount = int(math.ceil(cancel_amount / 100.0)) * 100
        # return cancel_amount
        return None

    def __str__(self):
        return f"{self.user.username}, {self.membership_payment}"

    class Meta:
        verbose_name = '유저 멤버십'
        verbose_name_plural = '유저 멤버십'
