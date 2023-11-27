import random

import rstr
from django.conf import settings
from django.db import models

import requests
from imagekit.models import ProcessedImageField

from weapon.core.utils import send_sms


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    image = ProcessedImageField(upload_to='uploads/profile/%Y/%m/%d/',
                                default="",
                                format='JPEG',
                                blank=True,
                                options={'quality': 60})

    is_first_visit = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    company = models.CharField(max_length=100, default="", blank=True)
    phone_number = models.CharField(verbose_name='phone_number', max_length=11, blank=True)
    kakao_thumbnail = models.CharField(max_length=100, default="", blank=True)
    recommend_code = models.CharField(max_length=5, default="", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.user.email}, {self.user.username}"


class PhoneNumber(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    phone_number = models.CharField(verbose_name='phone_number', max_length=11, blank=True)
    is_verified = models.BooleanField(default=False)
    code = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number}, {self.code}"

    def save(self, *args, **kwargs):
        # code initialization
        is_initialized = False
        if self.code == 0:
            self.code = random.randint(1000, 9999)
            is_initialized = True
        super(PhoneNumber, self).save(*args, **kwargs)

        if is_initialized:
            mesg = f"인증 번호 [{self.code}]를 입력해주세요."
            send_sms([self.phone_number], mesg)


class RequestDeleteUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '회원 탈퇴 요청'
        verbose_name_plural = '회원 탈퇴 요청'


class RecommendUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommend_user",
    )

    recommend_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommend_me_users",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '추천인'
        verbose_name_plural = '추천인'
