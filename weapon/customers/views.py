import datetime

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from weapon.core.utils import send_sms
from weapon.customers.calculate import calculate_total_analysis
from weapon.customers.models import Customer, CustomerMedicalHistory, CustomerGroup
from weapon.customers.serializers import CustomerSerializer, CustomerMedicalHistorySerializer, \
    CustomerSerializerWithInsuranceCount, CustomerGroupSerializerWithInsuranceCount, CustomerSerializerForDetail
from weapon.insurances.models import CustomerInsurance, CustomerInsuranceDetail, InsuranceDetail, AnalysisDetail, \
    ChartDetail
from weapon.insurances.serializers import CustomerInsuranceSerializer
from django.core.files.storage import FileSystemStorage
import os


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            instance.user_view_at = datetime.datetime.now()
            instance.save()

        serializer = CustomerSerializerForDetail(instance)
        return Response(serializer.data)

    def list(self, request):
        user = request.user
        keyword = self.request.query_params.get('keyword', None)

        if not keyword:
            queryset = self.filter_queryset(self.get_queryset()).filter(user=user, is_agree_term=True).order_by(
                '-created_at')
        if keyword:
            queryset = self.filter_queryset(self.get_queryset()).filter(Q(Q(user=user, is_agree_term=True), (
                Q(name__icontains=keyword) | Q(birth_day__icontains=keyword)))).order_by(
                '-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def last_view_list(self, request):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset()).filter(user=user, is_agree_term=True).order_by(
            '-user_view_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomerSerializerWithInsuranceCount(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomerSerializerWithInsuranceCount(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        now = datetime.datetime.now()

        user_membership = user.user_memberships.filter(is_churned=False, expiry_at__gte=now).order_by(
            '-created_at').first()
        if not user_membership:
            remain_add_user_count = 10 - len(user.customers.filter(is_agree_term=True))
            if remain_add_user_count <= 0:
                return Response('무료 기간에는 고객을 10명 까지 추가할 수 있습니다.', status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        id = serializer.data.get('id')
        instance = Customer.objects.get(id=id)
        instance.user_view_at = datetime.datetime.now()
        instance.save()

        mobile_phone_number = serializer.data.get('mobile_phone_number')
        customer_id = serializer.data.get('id')
        url = 'https://foliio.co.kr/customer/' + str(customer_id) + '/agree'
        message = '[폴리오] 개인 정보 수집 및 이용 동의\n\n▶ 아래 링크를 클릭해 동의를 완료해 주세요. \n' + url
        title = '[폴리오] 개인 정보 수집 및 이용 동의'
        send_sms([mobile_phone_number], message, title)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        is_agree_term = request.data.get('is_agree_term', None)
        if is_agree_term:
            phone_number = instance.user.profile.phone_number
            if phone_number:
                url = f'https://foliio.co.kr/customer/{instance.id}'
                message = f'[폴리오] {instance.name}님의 동의가 완료 되었어요!'
                title = f'[폴리오] {instance.name}님의 동의가 완료 되었어요!'
                send_sms([phone_number], message, title)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def update_group_customer(self, request, pk, **kwargs):
        instance = self.get_object()
        group_customers = request.data['group_customers']
        before_child_id_list = list(instance.child_customers.all().values_list('child_customer', flat=True))
        delete_list = before_child_id_list

        for child_customer_id in group_customers:
            if child_customer_id in before_child_id_list:
                delete_list.pop(delete_list.index(child_customer_id))

            else:
                customer_group = CustomerGroup()
                customer_group.parent_customer = instance
                customer_group.child_customer_id = child_customer_id
                customer_group.save()

        CustomerGroup.objects.filter(parent_customer=instance, child_customer_id__in=delete_list).delete()
        serializer = CustomerSerializerForDetail(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def medical_history_list(self, request, pk, **kwargs):
        instance = self.get_object()
        medical_histories_instance = instance.medical_histories.all()
        serializer = CustomerMedicalHistorySerializer(medical_histories_instance, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def insurance_list(self, request, pk, **kwargs):
        instance = self.get_object()
        portfolio_type = request.query_params.get('portfolio_type', None)
        keyword = request.query_params.get('keyword', None)
        queryset = instance.customer_insurance_list.all().order_by('-user_view_at')
        if portfolio_type:
            queryset = queryset.filter(portfolio_type=portfolio_type)
        if keyword:
            queryset = queryset.filter(name__contains=keyword)

        insurance_list = queryset.order_by('-user_view_at')

        page = self.paginate_queryset(insurance_list)
        if page is not None:
            serializer = CustomerInsuranceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomerInsuranceSerializer(insurance_list, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def group_customer_list(self, request, pk, **kwargs):
        instance = self.get_object()
        customer_group_instance_list = instance.child_customers.all()
        serializer = CustomerGroupSerializerWithInsuranceCount(customer_group_instance_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def copy_insurance(self, request, pk):
        instance = self.get_object()
        user = request.user

        customer_insurance_id_list = request.data.get('customer_insurance_list')
        portfolio_type = request.data.get('portfolio_type')

        customer_insurance_list = CustomerInsurance.objects.filter(id__in=customer_insurance_id_list)

        for customer_insurance in customer_insurance_list:
            with transaction.atomic():
                case_instance_list = customer_insurance.case_list.all()

                customer_insurance.id = None
                customer_insurance.portfolio_type = portfolio_type
                customer_insurance.customer = instance
                customer_insurance.user = user
                customer_insurance.is_template = False
                customer_insurance.is_common = False
                customer_insurance.save()

                for case_instance in case_instance_list:
                    case_instance.pk = None
                    case_instance.insurance = customer_insurance

                CustomerInsuranceDetail.objects.bulk_create(case_instance_list, 100)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)  # 통합분석
    def analysis(self, request, pk):
        customer_insurance_id = request.query_params.get('customer_insurance')
        instance = self.get_object()
        if customer_insurance_id:
            customer_insurance_list = instance.customer_insurance_list.filter(id=int(customer_insurance_id))
        else:
            customer_insurance_list = instance.customer_insurance_list.filter(portfolio_type=1)
        # insurance_type_list = [0]
        #
        # for customer_insurance in customer_insurance_list:
        #     if customer_insurance.insurance_type not in insurance_type_list:
        #         insurance_type_list.append(customer_insurance.insurance_type)

        chart_list = ChartDetail.objects.all().order_by('order').values()
        case_list = AnalysisDetail.objects.all().values()

        result = calculate_total_analysis(instance.birth_day, case_list, chart_list, customer_insurance_list)

        chart_one = {
            'name': [],
            'total_premium': [],
            'chart_based_amount': [],
            'percent': [],
            'colors': [],
        }

        # 실손 의료비
        chart_two = {
            'name': [],
            'total_premium': [],
            'chart_based_amount': [],
            'percent': [],
            'colors': [],
        }

        for case in result.get('chart_list'):
            name = case.get('name')
            if name == '상해후유장애':
                name = ['상해후유장애', '  (재해상해)']

            color = '#143243'
            if case['total_premium'] == 0:
                percent = 0
            elif case['total_premium'] > case.get('chart_based_amount'):
                percent = 100
                color = '#FF60B6'
            else:
                percent = (case['total_premium'] / case.get('chart_based_amount')) * 100

            if case.get('chart_type') == 1:
                chart_one['name'].append(name)
                chart_one['percent'].append(percent)
                chart_one['colors'].append(color)
            if case.get('chart_type') == 2:
                chart_two['name'].append(name)
                chart_two['percent'].append(percent)
                chart_two['colors'].append(color)

        result['customer'] = CustomerSerializer(instance).data
        result['chart_one'] = chart_one
        result['chart_two'] = chart_two

        return Response(result, status=status.HTTP_200_OK)
        # 해당 커스터머의 보험을 가지고 온다

    @action(methods=['get'], detail=True)  # 비교분석
    def compare(self, request, pk):
        instance = self.get_object()

        # 기존 리스트
        existing_list = instance.customer_insurance_list.filter(portfolio_type=1)
        # 제안 리스트
        suggest_list = instance.customer_insurance_list.filter(portfolio_type=2)

        # 제안 기존 나눠서
        # 월보험료, 합계, 총보험료, 합계, 기존낼돈, 제안낼돈, 기존혜약환급금 차액

        # 기존 낼돈
        # 제안 낼돈
        # 낼돈 = 총 보험료 - 낸돈 total_premiums - prepaid_insurance_premium

        # 1. 총 보험료 차액 계산의 "차액"금액을 N% 수익률로 복리계산 해주시면 됩니다.
        # 2. N% 수익률(왼쪽 상단)의 기본값은 4%이되 사용자가 -,+ 버튼을 눌러 조절 가능합니다.

        # + 오른쪽 상단의 기존, 제안 글자는 삭제해 주세요!
        # + 총 보험료 차액 계산의 "기존 낼 돈"은 종합 분석 결과의 "남은 돈" 입니다, 헷갈리실 것 같아서요!

        # 각 케이스 기존, 제안 나눠서 나이 별로 나누기
        # amount_list [0~10] 이중배열
        # case_list
        # - 기존
        #   - 합계
        #   - 비갱 합
        #   - 갱 합
        #   - 갱신 amount_list
        #   - 비갱신 amount_list
        # - 제안
        #   - 합계
        #   - 비갱 합
        #   - 갱 합
        #   - 갱신 amount_list
        #   - 비갱신 amount_list
        # - 자산 변동추이
        #   기존 제안 모든 케이스의 나이별로 합계

        # 사망 · 후유장애 · 진단비 · 운전자 · 기타
        chart_list = ChartDetail.objects.all().order_by('order').values()
        chart_list2 = ChartDetail.objects.all().order_by('order').values()
        case_list = AnalysisDetail.objects.all().values()
        case_list2 = AnalysisDetail.objects.all().values()
        existing_result = calculate_total_analysis(instance.birth_day, case_list, chart_list, existing_list)
        suggest_result = calculate_total_analysis(instance.birth_day, case_list2, chart_list2, suggest_list)

        # 월보험료
        monthly_existing_sum_premium = existing_result.get('monthly_premiums')
        monthly_suggest_sum_premium = suggest_result.get('monthly_premiums')
        monthly_calculate_premium = monthly_existing_sum_premium - monthly_suggest_sum_premium
        # 총보험료
        total_existing_sum_premium = existing_result.get('total_premiums')
        total_suggest_sum_premium = suggest_result.get('total_premiums')
        total_calculate_premium = total_existing_sum_premium - total_suggest_sum_premium

        total_cancellation_refund = existing_result.get('total_cancellation_refund')  # 기존 해약 환급금
        existing_pay_insurance_premium = existing_result.get('total_pay_insurance_premium')
        suggest_pay_insurance_premium = suggest_result.get('total_pay_insurance_premium')
        total_calculate = existing_pay_insurance_premium - suggest_pay_insurance_premium + total_cancellation_refund

        chart_one = {
            'name': [],
            'existing_percent': [],
            'suggest_percent': [],
        }

        # 실손 의료비
        chart_two = {
            'name': [],
            'existing_percent': [],
            'suggest_percent': [],
        }

        for case in existing_result.get('chart_list'):
            name = case.get('name')
            if case['total_premium'] == 0:
                percent = 0
            elif case['total_premium'] > case.get('chart_based_amount'):
                percent = 100
            else:
                percent = (case['total_premium'] / case.get('chart_based_amount')) * 100

            if case.get('chart_type') == 1:
                chart_one['name'].append(name)
                chart_one['existing_percent'].append(percent)
            if case.get('chart_type') == 2:
                chart_two['name'].append(name)
                chart_two['existing_percent'].append(percent)

        for case in suggest_result.get('chart_list'):
            if case['total_premium'] == 0:
                percent = 0
            elif case['total_premium'] > case.get('chart_based_amount'):
                percent = 100
            else:
                percent = (case['total_premium'] / case.get('chart_based_amount')) * 100

            if case.get('chart_type') == 1:
                chart_one['suggest_percent'].append(percent)
            if case.get('chart_type') == 2:
                chart_two['suggest_percent'].append(percent)

        result = {
            'customer': CustomerSerializer(instance).data,
            'monthly_existing_sum_premium': monthly_existing_sum_premium,
            'monthly_suggest_sum_premium': monthly_suggest_sum_premium,
            'total_existing_sum_premium': total_existing_sum_premium,
            'total_suggest_sum_premium': total_suggest_sum_premium,
            'total_cancellation_refund': total_cancellation_refund,
            'existing_pay_insurance_premium': existing_pay_insurance_premium,
            'suggest_pay_insurance_premium': suggest_pay_insurance_premium,
            'total_calculate': total_calculate,
            'total_calculate_premium': total_calculate_premium,
            'monthly_calculate_premium': monthly_calculate_premium,
            'chart_one': chart_one,
            'chart_two': chart_two,
            'existing': existing_result,
            'suggest': suggest_result,
        }

        return Response(result, status=status.HTTP_200_OK)
    # jhpark_20231221_S
    # 클라이언트에서 업로드 요청온 PDF 파일을 저장
    @action(methods=['post'], detail=True)
    def uploadimage(self, request, pk):
        # ID 값 검증
        id_value = request.data.get('id')
        if not id_value:
            return Response({'detail': 'ID를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 파일 검증
        if 'file' not in request.FILES:
            return Response({'detail': '파일을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        fs = FileSystemStorage()

        file = request.FILES['file']
        # 파일 저장
        filename = f'{id_value}_{file.name}'

        current_path = os.getcwd()
        media_folder = os.path.join(current_path, 'weapon/media')

        # 'media' 폴더 내의 PDF 파일 경로
        img_filepath = os.path.join(media_folder, filename)

        if fs.exists(img_filepath):
            fs.delete(img_filepath)

        filedata = fs.save(filename, file)
        file_url = fs.url(filedata)

        return Response({'detail': filedata}, status=status.HTTP_200_OK)
    # jhpark_20231221_E



class CustomerMedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = CustomerMedicalHistory.objects.all()
    serializer_class = CustomerMedicalHistorySerializer


