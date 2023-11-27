from django.conf import settings
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    MOBILE_PHONE_CARRIER_TYPE = (
        (0, None),
        (1, 'KT'),
        (2, 'SKT'),
        (3, 'LGU+'),
        (4, 'KT 알뜰폰'),
        (5, 'SKT 알뜰폰'),
        (6, 'LGU+ 알뜰폰'),
    )
    MOBILE_PHONE_CARRIER_TYPE_DICT = {v: k for k, v in MOBILE_PHONE_CARRIER_TYPE}

    DRIVE_TYPE = (
        (0, None),
        (1, '자가용'),
        (2, '영업용'),
        (3, '비운전자'),
    )
    DRIVE_TYPE_DICT = {v: k for k, v in DRIVE_TYPE}

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers')
    mobile_phone_number = models.CharField('연락처', max_length=15, default="")
    name = models.CharField(max_length=20)

    # optional
    is_agree_term = models.BooleanField('동의 여부', default=False, blank=True)
    birth_day = models.CharField('생일', max_length=10, blank=True, default='')
    mobile_phone_carrier = models.SmallIntegerField('통신사', choices=MOBILE_PHONE_CARRIER_TYPE, default=None, null=True, blank=True)
    phone_number = models.CharField('전화번호', max_length=15, blank=True, default='')
    address = models.CharField('주소', max_length=100, blank=True, default='')
    job = models.CharField('직업', max_length=20, blank=True, default='')
    # is_drive = models.BooleanField('운전여부', blank=True, default=None, null=True)
    drive_type = models.SmallIntegerField('운전여부', choices=DRIVE_TYPE, default=None, null=True, blank=True)
    business_type = models.CharField('업종', max_length=20, blank=True, default='')
    memo = models.TextField('메모', blank=True, default='')
    email = models.CharField('이메일', max_length=50, blank=True, default='')
    company = models.CharField('회사명', max_length=100, blank=True, default='')
    drink_bottle = models.SmallIntegerField('음주 병수', blank=True, default=0)
    drink_week = models.SmallIntegerField('음주 한주 횟수', blank=True, default=0)
    smoke_daily = models.SmallIntegerField('흡연 일일 횟수', blank=True, default=0)
    smoke_years = models.SmallIntegerField('흡연 년수', blank=True, default=0)
    height = models.SmallIntegerField('키', blank=True, default=0)
    weight = models.SmallIntegerField('몸무게', blank=True, default=0)
    baby_due_date = models.CharField('출산 에정일', max_length=10, blank=True, default='')
    relate_name = models.CharField('관계', max_length=10, blank=True, default='')
    legal_representative_name = models.CharField('법정 대리인', max_length=5, blank=True, default='')
    user_view_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '고객'
        verbose_name_plural = '고객'


# 고객 병력
class CustomerMedicalHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='medical_histories')
    is_inpatient = models.BooleanField('입원여부')
    diagnostic_name = models.CharField('진단명', max_length=100)
    treatment_content = models.CharField('치료 내용', max_length=100)
    hospital_name = models.CharField('병원명', max_length=100, blank=True, default='')
    treatment_start_date = models.CharField('치료 시작일', max_length=10, blank=True, default='')
    treatment_end_date = models.CharField('치료 종료일', max_length=10, blank=True, default='')
    is_recurrence = models.BooleanField('재발여부', blank=True, default=None, null=True)
    is_cure = models.BooleanField('완치여부', blank=True, default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.diagnostic_name

    class Meta:
        verbose_name = '고객 병력'
        verbose_name_plural = '고객 병력'


class CustomerGroup(models.Model):
    parent_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='child_customers')
    child_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='parent_customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '고객 그룹'
        verbose_name_plural = '고객 그룹'
