import datetime

import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField

from weapon.customers.models import Customer



class AnalysisCategory(models.Model):
    INSURANCE_TYPE = (
        (0, '공통'),
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}

    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=0)
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)

    def __str__(self):
        return f'{self.order}, {self.name}'

    class Meta:
        verbose_name = '분석 카테고리'
        verbose_name_plural = '분석 카테고리'


class AnalysisSubCategory(models.Model):
    INSURANCE_TYPE = (
        (0, '공통'),
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}

    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=0)
    category = models.ForeignKey(AnalysisCategory, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)

    def __str__(self):
        return f'{self.category.name} / {self.order}, {self.name}'

    class Meta:
        verbose_name = '분석 서브 카테고리'
        verbose_name_plural = '분석 서브 카테고리'


class AnalysisDetail(models.Model):
    sub_category = models.ForeignKey(AnalysisSubCategory, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)
    chart_based_amount = models.SmallIntegerField('차트 기준 금액', default=0, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '분석 상세 아이템'
        verbose_name_plural = '분석 상세 아이템'


class ChartDetail(models.Model):
    CHART_TYPE = (
        (1, 'Cart1'),
        (2, 'Cart2'),
    )
    CHART_TYPE_DICT = {v: k for k, v in CHART_TYPE}

    INSURANCE_TYPE = (
        (0, '공통'),
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}

    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=0)
    chart_type = models.SmallIntegerField(choices=CHART_TYPE, default=1)
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)
    chart_based_amount = models.SmallIntegerField('차트 기준 금액', default=0, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '분석 차트 아이템'
        verbose_name_plural = '분석 차트 아이템'


class InsuranceTag(models.Model):
    name = models.CharField(max_length=45, primary_key=True)

    class Meta:
        verbose_name = '보험 태그'
        verbose_name_plural = '보험 태그'

    def __str__(self):
        return self.name


class InsuranceCategory(models.Model):
    INSURANCE_TYPE = (
        (0, '공통'),
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}

    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=0)
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)

    def __str__(self):
        return f'{self.order}, {self.name}'

    class Meta:
        verbose_name = '보험 카테고리'
        verbose_name_plural = '보험 카테고리'


class InsuranceSubCategory(models.Model):
    INSURANCE_TYPE = (
        (0, '공통'),
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}

    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=0)
    category = models.ForeignKey(InsuranceCategory, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)

    def __str__(self):
        return f'{self.category.name} / {self.insurance_type} / {self.name}'

    class Meta:
        verbose_name = '보험 서브 카테고리'
        verbose_name_plural = '보험 서브 카테고리'


class InsuranceDetail(models.Model):
    CHART_TYPE = (
        (1, 'Cart1'),
        (2, 'Cart2'),
    )
    CHART_TYPE_DICT = {v: k for k, v in CHART_TYPE}

    chart_type = models.SmallIntegerField(choices=CHART_TYPE, default=1)

    sub_category = models.ForeignKey(InsuranceSubCategory, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)
    chart_based_amount = models.SmallIntegerField('차트 기준 금액', default=0, blank=True)
    analysis_detail = models.ManyToManyField(AnalysisDetail)
    chart_detail = models.ManyToManyField(ChartDetail)

    def __str__(self):
        return f'{self.sub_category.category.name} / {self.sub_category.name} / {self.order}, {self.name}'

    class Meta:
        verbose_name = '보험 상세 아이템'
        verbose_name_plural = '보험 상세 아이템'


class Insurance(models.Model):
    name = models.CharField('보험명', max_length=20)
    order = models.SmallIntegerField('순서', default=0, blank=True)
    image = ProcessedImageField(upload_to='uploads/insurance/%Y/%m/%d/',
                                default="",
                                format='JPEG',
                                options={'quality': 100})
    INSURANCE_TYPE = (
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}

    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=1)


    def __str__(self):
        return f'{self.order}, {self.name}'

    class Meta:
        verbose_name = '보험'
        verbose_name_plural = '보험'


class CustomerInsurance(models.Model):
    PORTFOLIO_TYPE = (
        (0, '템플릿'),
        (1, '기존'),
        (2, '제안'),
    )
    PORTFOLIO_TYPE_DICT = {v: k for k, v in PORTFOLIO_TYPE}

    INSURANCE_TYPE = (
        (1, '생명보험'),
        (2, '손해보험'),
    )
    INSURANCE_TYPE_DICT = {v: k for k, v in INSURANCE_TYPE}
    PAYMENT_PERIOD_TYPE = (
        (1, '년'),
        (2, '년 갱신'),
    )
    PAYMENT_PERIOD_TYPE_DICT = {v: k for k, v in PAYMENT_PERIOD_TYPE}
    WARRANTY_PERIOD_TYPE = (
        (1, '세 만기'),
        (2, '년 만기'),
        (3, '종신'),
    )
    WARRANTY_PERIOD_TYPE_DICT = {v: k for k, v in WARRANTY_PERIOD_TYPE}

    REFUND_TYPE = (
        (1, '종신보험'),
        (2, '만기환급'),
        (3, '50%환급'),
        (4, '순수보장형'),
    )
    REFUND_TYPE_DICT = {v: k for k, v in REFUND_TYPE}

    is_common = models.BooleanField('공통 유무', default=False)  # 어드민용

    insurance = models.ForeignKey(Insurance, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None, null=True, blank=True,
                                 related_name="customer_insurance_list")
    insurance_type = models.SmallIntegerField(choices=INSURANCE_TYPE, default=1)

    name = models.CharField('상품명', max_length=100, default=None, null=True, blank=True)
    contractor_name = models.CharField('계약자 이름', max_length=10, default=None, null=True, blank=True)
    insured_name = models.CharField('피보험자 이름', max_length=10, default=None, null=True, blank=True)
    is_same_insured = models.BooleanField('계/피 동일', default=None, null=True, blank=True)
    portfolio_type = models.SmallIntegerField('포트폴리오 타입', choices=PORTFOLIO_TYPE, default=0)
    payment_period_type = models.SmallIntegerField('납입기간 타입', choices=PAYMENT_PERIOD_TYPE, default=1)
    warranty_period_type = models.SmallIntegerField('보장기간 타입', choices=WARRANTY_PERIOD_TYPE, default=1)
    payment_period = models.IntegerField('납입기간', default=None, null=True, blank=True)
    warranty_period = models.IntegerField('보장기간', default=None, null=True, blank=True)
    contract_date = models.CharField('계약일', max_length=10, default=None, null=True, blank=True)
    expiry_date = models.CharField('만기일', max_length=10, default=None, null=True, blank=True)
    old = models.IntegerField('나이', default=None, null=True, blank=True)  # 자주쓰는

    renewal_month = models.IntegerField('총 갱신 납입 회차', default=None, null=True, blank=True)
    non_renewal_month = models.IntegerField('총 비갱신 납입 회차', default=None, null=True, blank=True)
    monthly_assurance_premium = models.IntegerField('월 보장 보험료', default=None, null=True, blank=True)
    monthly_special_premium = models.IntegerField('월 특약 보험료', default=None, null=True, blank=True)
    monthly_premiums = models.IntegerField('월 납입 보험료', default=None, null=True, blank=True)
    monthly_contract_premium = models.IntegerField('월 주계약 보험료', default=None, null=True, blank=True)
    monthly_earned_premium = models.IntegerField('월 적립 보험료', default=None, null=True, blank=True)

    monthly_non_renewal_premium = models.IntegerField('월 비갱신 보험료', default=None, null=True, blank=True)
    monthly_renewal_premium = models.IntegerField('월 갱신 보험료', default=None, null=True, blank=True)

    # 계산되는 부분
    total_premiums = models.FloatField('총 납입 보험료', default=None, null=True, blank=True)
    total_renewal_premium = models.FloatField('총 갱신 보험료', default=None, null=True, blank=True)
    total_non_renewal_premium = models.FloatField('총 비갱신 보험료', default=None, null=True, blank=True)
    total_earned_premium = models.FloatField('총 적립 보험료', default=None, null=True, blank=True)
    expected_due_year = models.IntegerField('예상 만기 년수', default=None, null=True, blank=True)  # 년만기 보장 기간, 세 만기 나이 - 보장 기간

    cancellation_refund = models.IntegerField('혜약 환급금', default=None, null=True, blank=True)
    refund_type = models.SmallIntegerField('환급타입', choices=REFUND_TYPE, default=1)
    percent_cancellation_refund = models.IntegerField('혜약 환급금 퍼센트', default=None, null=True, blank=True)

    renewal_growth_rate = models.IntegerField('갱신 증가율', default=None, null=True, blank=True)
    renewal_special_expiry_date = models.CharField('갱신특약 만기일 날짜', max_length=10, default=None, null=True, blank=True)
    renewal_special_expiry = models.IntegerField('갱신특약 만기일', default=None, null=True, blank=True)
    user_view_at = models.DateTimeField(default=None, null=True, blank=True)
    comment_title = models.CharField(max_length=100, default=None, null=True, blank=True)
    comment = models.TextField(default=None, null=True, blank=True)
    is_template = models.BooleanField(default=False)

    tags = models.ManyToManyField(InsuranceTag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '포트폴리오'
        verbose_name_plural = '포트폴리오'

    def set_renewal_month(self):
        # if self.payment_period_type == 1:
        self.non_renewal_month = self.payment_period * 12
            # 계약일 만기일
            # date1 = datetime.datetime.strptime(self.contract_date, '%Y.%m.%d')
            # date2 = datetime.datetime.strptime(self.expiry_date, '%Y.%m.%d')
            # r = relativedelta(date2, date1)
            # renewal_month = r.years * 12 + r.months
            # self.renewal_month = renewal_month + 1

        # 년 갱신 인경우
        # if self.payment_period_type == 2:
            # 손해보험 보험
        # self.non_renewal_month = None

        if self.contract_date:
            if self.insurance_type == 2:
                date1 = datetime.datetime.strptime(self.contract_date, '%Y.%m.%d')
                date2 = datetime.datetime.strptime(self.expiry_date, '%Y.%m.%d')
                r = relativedelta(date2, date1)
                renewal_month = r.years * 12 + r.months
                self.renewal_month = renewal_month

            # 생명 보험
            if self.insurance_type == 1:
                date1 = datetime.datetime.strptime(self.contract_date, '%Y.%m.%d')
                renewal_special_expiry = self.renewal_special_expiry

                if not renewal_special_expiry:
                    renewal_special_expiry = 100

                now = datetime.datetime.now()
                birth_day = self.customer.birth_day
                contract_date = self.contract_date
                date1 = datetime.datetime.strptime(birth_day, '%Y.%m.%d')
                date2 = datetime.datetime.strptime(contract_date, '%Y.%m.%d')
                old = relativedelta(now, date1).years + 1
                contract_old = old - (datetime.datetime.now().year - date2.year)
                expiry = renewal_special_expiry - contract_old

                now = datetime.datetime.now()
                expiry_date = now + relativedelta(years=expiry)

                renewal_date = relativedelta(expiry_date, date2)

                renewal_month = renewal_date.years * 12 + renewal_date.months

                self.renewal_month = renewal_month

        else:
            self.renewal_month = self.expected_due_year * 12

        self.save()

    def calculate(self):
        monthly_renewal_premium = 0  # 월 비갱신 보험료
        monthly_non_renewal_premium = 0  # 월 비갱신 보험료
        total_premiums = 0  # 총 납입 보험료
        total_renewal_premium = 0  # 총 갱신 보험료
        total_non_renewal_premium = 0  # 총 비갱신 보험료
        total_earned_premium = 0  # 총 적립 보험료
        monthly_earned_premium = 0  # 월 적립 보험료
        if self.monthly_earned_premium:
            monthly_earned_premium = self.monthly_earned_premium
        # 총 적립금 = 월 적립금 * 납입기간 * 12 (납입 타입이 년 인경우, 년 갱신 0)
        if self.payment_period_type == 1:
            total_earned_premium = monthly_earned_premium * self.non_renewal_month

        # 총 보험료 계산
        # 담보 보험료 x - 손해 보험 - 년
        # 담보 보험료 x - 손해 보험 - 년 갱신
        # 담보 보험료 x - 생명 보험 - 년
        # 담보 보험료 x - 생명 보험 - 년 갱신

        # 담보 보험료 o - 담보별 년
        # 담보 보험료 o - 담보별 세
        # 담보 보험료 o - 담보별 년 갱신

        # ================= 보험료 케이스 별 계산 ====================================================

        case_list = self.case_list.all()

        for case in case_list:
            if case.total_renewal_premium:
                monthly_renewal_premium = monthly_renewal_premium + case.premium
                total_renewal_premium = total_renewal_premium + case.total_renewal_premium
            if case.total_non_renewal_premium:
                monthly_non_renewal_premium = monthly_non_renewal_premium + case.premium
                total_non_renewal_premium = total_non_renewal_premium + case.total_non_renewal_premium

        if monthly_renewal_premium == 0 and self.monthly_renewal_premium:
            monthly_renewal_premium = self.monthly_renewal_premium

        if total_renewal_premium > 0 or total_non_renewal_premium > 0:  # 담보별 가격이 있음
            # @ 담보 보험료 o - 담보별 년
            # @ 담보 보험료 o - 담보별 세
            # @ 담보 보험료 o - 담보별 년 갱신
            if self.insurance_type == 1:  # 생명보험
                etc_premium = self.monthly_premiums - monthly_non_renewal_premium - monthly_renewal_premium
                total_etc_premium = etc_premium * self.non_renewal_month
                total_premiums = total_non_renewal_premium + total_renewal_premium + total_etc_premium
            else:  # 손해 보험
                etc_premium = self.monthly_premiums - monthly_non_renewal_premium - monthly_renewal_premium - monthly_earned_premium
                total_etc_premium = etc_premium * self.non_renewal_month
                total_premiums = total_non_renewal_premium + total_renewal_premium + total_earned_premium + total_etc_premium

        else:
            if self.insurance_type == 2:  # 손해보험
                # @ 담보 보험료 x - 손해 보험 - 년

                # Rate는 기간당 이자율입니다.  갱신 증가율 * 12
                # Nper는 연금의 총 지급 기간입니다.  갱신 개월수
                # Pmt는 각 기간마다 지급되는 지급액이며, 연금 연수에 따라 변경될 수 없습니다. Pmt는 음수로 입력해야 합니다.
                # Pv는 현재 가치 또는 일련의 미래 지급 가치가 있는 일시불 금액입니다. pv를 생략하면 0으로 가정합니다. PV는 음수로 입력해야 합니다.
                # numpy.fv(Rate, Nper, Pmt, Pv)
                if self.renewal_month and self.renewal_growth_rate and self.monthly_renewal_premium:
                    total_renewal_premium = round(-npf.fv((self.renewal_growth_rate / 100) / 12, self.renewal_month,
                                                        self.monthly_renewal_premium, 0), 0)

                if self.payment_period_type == 1:  # 년
                    # 갱신 총 납입 횟수 = 만기일 - 계약일 개월수
                    renewal_month = 0
                    # 비갱신 총 납입 횟수 = 납입기간 * 12
                    non_renewal_month = self.payment_period * 12
                    # 월 비갱신 보험료 = 월 보장 보험료 - 월 갱신 보험료
                    monthly_non_renewal_premium = self.monthly_assurance_premium - monthly_renewal_premium

                    # 총 비갱신 = 비갱신 납입 개월 * 월 비갱신 보험료
                    total_non_renewal_premium = non_renewal_month * monthly_non_renewal_premium
                    # 총 보험료 = 총 비갱신 + 총 갱신 + 총 적립
                    total_premiums = total_earned_premium + total_renewal_premium + total_non_renewal_premium

                # @ 담보 보험료 x - 손해 보험 - 년 갱신
                if self.payment_period_type == 2:  # 년 갱신
                    total_premiums = total_renewal_premium

            if self.insurance_type == 1:  # 생명보험
                # @ 담보 보험료 x - 생명 보험 - 년
                if self.payment_period_type == 1:  # 년
                    # 총 비용 = 월 보험료 * 납입기간 * 12
                    non_renewal_month = self.payment_period * 12
                    total_premiums = self.monthly_premiums * non_renewal_month
                    monthly_non_renewal_premium = self.monthly_premiums - self.monthly_earned_premium
                    total_non_renewal_premium = non_renewal_month * monthly_non_renewal_premium
                    total_renewal_premium = 0
                    monthly_renewal_premium = 0

                # @ 담보 보험료 x - 생명 보험 - 년 갱신
                if self.payment_period_type == 2:  # 년 갱신
                    monthly_renewal_premium = self.monthly_premiums
                    total_renewal_premium = round(-npf.fv((self.renewal_growth_rate / 100) / 12, self.renewal_month,
                                              monthly_renewal_premium, 0), 0)
                    total_premiums = total_renewal_premium
                    monthly_earned_premium = 0
                    monthly_non_renewal_premium = 0
                    total_earned_premium = 0
                    total_non_renewal_premium = 0

        self.total_premiums = total_premiums
        self.monthly_non_renewal_premium = monthly_non_renewal_premium
        self.monthly_renewal_premium = monthly_renewal_premium
        self.total_renewal_premium = total_renewal_premium
        self.total_non_renewal_premium = total_non_renewal_premium
        self.total_earned_premium = total_earned_premium
        self.monthly_earned_premium = monthly_earned_premium


class CustomerInsuranceDetail(models.Model):
    insurance = models.ForeignKey(CustomerInsurance, on_delete=models.CASCADE, related_name="case_list")
    detail = models.ForeignKey(InsuranceDetail, on_delete=models.CASCADE)

    PAYMENT_PERIOD_TYPE = (
        (1, '년'),
        (2, '세'),
        (3, '년 갱신'),
    )
    PAYMENT_PERIOD_TYPE_DICT = {v: k for k, v in PAYMENT_PERIOD_TYPE}
    WARRANTY_PERIOD_TYPE = (
        (1, '세'),
        (2, '년'),
        (3, '날짜'),
        (4, '종신'),
    )
    WARRANTY_PERIOD_TYPE_DICT = {v: k for k, v in WARRANTY_PERIOD_TYPE}

    assurance_amount = models.IntegerField('보장 금액', default=None, null=True, blank=True)
    premium = models.IntegerField('보험료', default=None, null=True, blank=True)
    payment_period_type = models.SmallIntegerField('납입기간 타입', choices=PAYMENT_PERIOD_TYPE, default=1)
    payment_period = models.IntegerField('납입기간', default=None, null=True, blank=True)
    warranty_period_type = models.SmallIntegerField('보증기간 타입', choices=WARRANTY_PERIOD_TYPE, default=1)
    warranty_period = models.CharField('보증기간', max_length=20, default=None, null=True, blank=True)  # 날짜도 가능해야 하기때문에

    total_renewal_premium = models.FloatField('총 갱신 보험료', default=None, null=True, blank=True)
    total_non_renewal_premium = models.FloatField('총 비갱신 보험료', default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.detail.name

    class Meta:
        verbose_name = '고객 보험 상세'
        verbose_name_plural = '고객 보험 상세'

    def calculate(self, insurance):
        self.total_renewal_premium = 0
        self.total_non_renewal_premium = 0

        if self.premium:
            if self.payment_period_type == 1:
                # 납입기간 타입 이 '년' 인경우
                self.total_non_renewal_premium = self.payment_period * 12 * self.premium
            if self.payment_period_type == 2:
                # 나이 계산
                # 납입기간 타입 이 '세' 인경우
                # 납입기간 = 보장기간 - 나이
                # case.비갱신합계 = 납입기간 * 12 * 보험료

                if insurance.customer:
                    birth_day = insurance.customer.birth_day
                    contract_date = insurance.contract_date
                    now = datetime.datetime.now()
                    date1 = datetime.datetime.strptime(birth_day, '%Y.%m.%d')
                    date2 = datetime.datetime.strptime(contract_date, '%Y.%m.%d')
                    old = relativedelta(now, date1).years + 1
                    contract_old = old - (datetime.datetime.now().year - date2.year)
                    old = contract_old
                else:
                    old = insurance.old

                period = self.payment_period - old
                self.total_non_renewal_premium = period * 12 * self.premium

            if self.payment_period_type == 3:
                # 납입기간 타입 이 '년 갱신' 인경우
                # 보험 총 납입 개월 수
                total_renewal_premium = round(-npf.fv((insurance.renewal_growth_rate / 100) / 12, insurance.renewal_month,
                                                 self.premium, 0), 0)
                self.total_renewal_premium = total_renewal_premium

# jhpark_20231229_S
# 보험 증권 테이블 추가
class MyModel(models.Model):
    insurance_content = models.TextField(max_length=500)

    def __str__(self):
        return self.insurance_content[:50]  # 객체를 문자열로 표현할 때 처음 50자만 표시
# jhpark_20231229_E

