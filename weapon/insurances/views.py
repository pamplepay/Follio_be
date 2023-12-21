import datetime

from django.db import transaction
from django.db.models import Q
from pytz import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from weapon.core.utils import convert_pdf_to_png
from weapon.core.utils import ocr_process

from weapon.customers.calculate import calculate_analysis
from weapon.customers.serializers import CustomerSerializer
from weapon.insurances.models import InsuranceCategory, Insurance, CustomerInsurance, CustomerInsuranceDetail, \
    InsuranceDetail, AnalysisDetail, AnalysisCategory, ChartDetail, AnalysisSubCategory, InsuranceSubCategory, \
    InsuranceTag
from weapon.insurances.serializers import InsuranceCategorySerializer, InsuranceSerializer, \
    CustomerInsuranceSerializer, CustomerInsuranceSerializerForDetail, AnalysisCategorySerializer

KST = timezone('Asia/Seoul')
UTC = timezone("UTC")


class CustomerInsuranceViewSet(viewsets.ModelViewSet):
    queryset = CustomerInsurance.objects.all()
    serializer_class = CustomerInsuranceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            instance.user_view_at = datetime.datetime.now()
            instance.save()

        serializer = CustomerInsuranceSerializerForDetail(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        with transaction.atomic():
            tags = request.data.get('tags', None)
            if tags:
                tag_name_list = InsuranceTag.objects.filter(name__in=tags).values_list('name', flat=True)
                for tag in tags:
                    if tag not in tag_name_list:
                        InsuranceTag.objects.create(name=tag)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            id = serializer.data.get('id')

            instance = CustomerInsurance.objects.get(id=id)
            instance.user_view_at = datetime.datetime.now()
            instance.set_renewal_month()
            instance.save()

            case_list = data.get('case_list')

            for case in case_list:
                detail = case.get('detail')
                assurance_amount = case.get('assurance_amount')
                premium = case.get('premium')
                payment_period_type = case.get('payment_period_type')
                payment_period = case.get('payment_period')
                warranty_period_type = case.get('warranty_period_type')
                warranty_period = case.get('warranty_period')

                if assurance_amount and payment_period:
                    customer_insurance_detail = CustomerInsuranceDetail()
                    customer_insurance_detail.insurance = instance
                    customer_insurance_detail.assurance_amount = assurance_amount
                    customer_insurance_detail.detail_id = detail
                    if premium:
                        customer_insurance_detail.premium = premium
                    customer_insurance_detail.payment_period_type = payment_period_type
                    if payment_period:
                        customer_insurance_detail.payment_period = payment_period
                    customer_insurance_detail.warranty_period_type = warranty_period_type
                    if warranty_period_type == 4:
                        customer_insurance_detail.warranty_period = None
                    else:
                        if warranty_period:
                            customer_insurance_detail.warranty_period = warranty_period

                    customer_insurance_detail.calculate(instance)
                    customer_insurance_detail.save()

            instance.calculate()
            instance.save()

        data = CustomerInsuranceSerializerForDetail(instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = self.request.data
        tags = data.get('tags', None)
        if tags:
            tag_name_list = InsuranceTag.objects.filter(name__in=tags).values_list('name', flat=True)
            for tag in tags:
                if tag not in tag_name_list:
                    InsuranceTag.objects.create(name=tag)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance = self.get_object()

        case_list = data.get('case_list')
        case_id_list = list(map(lambda x: x.get('id'), case_list))
        case_id_list = list(filter(lambda x: x is not None, case_id_list))
        delete_list = list(instance.case_list.all().values_list('id', flat=True))

        instance.set_renewal_month()

        if instance.insurance_type == 1:
            detail_list = CustomerInsuranceDetail.objects.filter(insurance=instance, detail__sub_category__insurance_type=2).all()
            detail_list.delete()
        else:
            detail_list = CustomerInsuranceDetail.objects.filter(insurance=instance, detail__sub_category__insurance_type=1).all()
            detail_list.delete()

        case_instance_list = CustomerInsuranceDetail.objects.filter(id__in=case_id_list)
        case_list_dict = {}
        case_id_list = []
        for case_instance in case_instance_list:
            case_list_dict[case_instance.id] = case_instance
            case_id_list.append(case_instance.id)

        for case in case_list:
            case_id = case.get('id')
            detail = case.get('detail')
            assurance_amount = case.get('assurance_amount')
            premium = case.get('premium')
            payment_period_type = case.get('payment_period_type')
            payment_period = case.get('payment_period')
            warranty_period_type = case.get('warranty_period_type')
            warranty_period = case.get('warranty_period')

            if case_id and case_id in case_id_list:
                if (not premium or premium == '') and (not payment_period or payment_period == '') and (not warranty_period or warranty_period == ''):
                    continue

                case_instance = case_list_dict[case_id]
                delete_list.pop(delete_list.index(case_id))

            else:
                case_instance = CustomerInsuranceDetail()
                case_instance.insurance = instance
                case_instance.detail_id = detail

            if assurance_amount and payment_period:
                case_instance.assurance_amount = assurance_amount
                if premium != '':
                    case_instance.premium = premium
                case_instance.payment_period_type = payment_period_type
                case_instance.payment_period = payment_period
                case_instance.warranty_period_type = warranty_period_type
                if warranty_period_type == 4:
                    case_instance.warranty_period = None
                else:
                    case_instance.warranty_period = warranty_period

                case_instance.calculate(instance)
                case_instance.save()

        if len(delete_list) > 0:
            CustomerInsuranceDetail.objects.filter(id__in=delete_list).delete()

        instance.calculate()
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        instance = self.get_object()
        return Response(CustomerInsuranceSerializerForDetail(instance).data)

    def list(self, request, *args, **kwargs):
        user = request.user

        keyword = self.request.query_params.get('keyword', None)

        if not keyword:
            queryset = self.filter_queryset(self.get_queryset()).filter(user=user)
        if keyword:
            queryset = self.filter_queryset(self.get_queryset()).filter(user=user, name__icontains=keyword).order_by('-is_common', '-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def last_view_list(self, request):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset()).filter(user=user).order_by('-user_view_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def last_view_template_list(self, request):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset()).filter(user=user, customer__isnull=True).order_by(
            '-user_view_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def template(self, request):
        user = request.user
        keyword = self.request.query_params.get('keyword', None)
        if not keyword:
            queryset = self.filter_queryset(self.get_queryset()).filter(
                Q(Q(user=user, portfolio_type=0) | Q(is_common=True))).order_by('-is_common', '-created_at')
        if keyword:
            queryset = self.filter_queryset(self.get_queryset()).filter(
                Q(Q(Q(user=user, portfolio_type=0) | Q(is_common=True)), Q(Q(name__icontains=keyword) | Q(tags__name__icontains=keyword)))).order_by('-is_common', '-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # jhpark_20231221_S
    # pdf 파일을 png 파일로 변경 후 ocr detect 처리
    @action(methods=['post'], detail=True)
    def detect(self, request, pk):
        info = request.data['info']
        print(info)
        png_path = convert_pdf_to_png(info)
        result = {}
        ocr_result = ocr_process(png_path)
        result['data'] = ocr_result
        return Response(result, status=status.HTTP_200_OK)
    # jhpark_20231221_E

    @action(methods=['get'], detail=True)
    def analysis(self, request, pk):
        instance = self.get_object()
        insurance_type_list = [0, instance.insurance_type]
        birth_day = None
        if instance.customer:
            birth_day = instance.customer.birth_day
        chart_list = ChartDetail.objects.filter(insurance_type__in=insurance_type_list).order_by('order').values()
        case_list = InsuranceDetail.objects.filter(sub_category__insurance_type__in=insurance_type_list).values()
        result = calculate_analysis(birth_day, case_list, chart_list, [instance])

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
            color = '#143243'

            if instance.insurance_type == 1 and case.get('id') == 1:
                name = '일반사망'
            if instance.insurance_type == 2 and case.get('id') == 1:
                name = '상해사망'
            if instance.insurance_type == 1 and case.get('id') == 2:
                name = '재해사망'
            if instance.insurance_type == 1 and name == '상해후유장애':
                name = '재해상해'

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

        if instance.customer:
            result['customer'] = CustomerSerializer(instance.customer).data
        else:
            result['customer'] = None
        result['chart_one'] = chart_one
        result['chart_two'] = chart_two
        result['insurance_type_list'] = insurance_type_list

        return Response(result, status=status.HTTP_200_OK)


class CommonInsuranceApiViewSet(APIView):
    def get(self, *args, **kwargs):
        category_list = InsuranceCategory.objects.order_by('order').values()
        category_dict = {}
        for category in category_list:
            category['sub_category_list'] = []
            category_dict[category['id']] = category
        sub_category_list = InsuranceSubCategory.objects.order_by('order').values()
        sub_category_dict = {}
        for sub_category in sub_category_list:
            sub_category['detail_list'] = []
            sub_category_dict[sub_category['id']] = sub_category
            category_dict[sub_category['category_id']]['sub_category_list'].append(sub_category)

        detail_list = InsuranceDetail.objects.order_by('order').values()
        for detail in detail_list:
            sub_category_dict[detail['sub_category_id']]['detail_list'].append(detail)

        analysis_category_list = AnalysisCategory.objects.order_by('order').values()
        analysis_category_dict = {}
        for category in analysis_category_list:
            category['sub_category_list'] = []
            analysis_category_dict[category['id']] = category
        analysis_sub_category_list = AnalysisSubCategory.objects.order_by('order').values()
        analysis_sub_category_dict = {}
        for sub_category in analysis_sub_category_list:
            sub_category['detail_list'] = []
            analysis_sub_category_dict[sub_category['id']] = sub_category
            analysis_category_dict[sub_category['category_id']]['sub_category_list'].append(sub_category)

        analysis_detail_list = AnalysisDetail.objects.order_by('order').values()
        for detail in analysis_detail_list:
            analysis_sub_category_dict[detail['sub_category_id']]['detail_list'].append(detail)

        insurance_list = Insurance.objects.all()

        result = {
            'insurance_list': InsuranceSerializer(insurance_list, many=True).data,
            'categories': category_list,
            'analysis_categories': analysis_category_list
        }

        return Response(result, status=status.HTTP_200_OK)
