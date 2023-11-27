import datetime

from dateutil.relativedelta import relativedelta

from weapon.insurances.serializers import CustomerInsuranceSerializer


def calculate_analysis(birth_day, case_list, chart_list, insurance_list):
    monthly_premiums = 0  # 월 납입 보험료
    monthly_renewal_premium = 0  # 월 갱신 보험료
    monthly_non_renewal_premium = 0  # 월 비갱신 보험료
    monthly_earned_premium = 0  # 월 적립 보험료
    total_premiums = 0  # 총 보험료
    total_renewal_premium = 0  # 총 갱신 보험료
    total_non_renewal_premium = 0  # 총 비갱신 보험료
    total_earned_premium = 0  # 총 적립 보험료
    total_cancellation_refund = 0  # 총 환급금
    total_cancellation_loss = 0  # 총 손실금
    total_prepaid_insurance_premium = 0
    total_pay_insurance_premium = 0

    case_list_index = {}
    chart_list_index = {}
    chart_id_list = []

    for index, case in enumerate(case_list):
        case['total_premium'] = 0
        case['total_renewal_premium'] = 0
        case['total_non_renewal_premium'] = 0
        case['non_renewal_old_list'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 무조건 10개
        case['renewal_old_list'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 무조건 10개
        case['total_premium_list'] = [0] * len(insurance_list)
        case['is_show_old_price'] = False
        case_list_index[case.get('id')] = index

    for index, case in enumerate(chart_list):
        case['total_premium'] = 0
        case['total_renewal_premium'] = 0
        case['total_non_renewal_premium'] = 0
        chart_list_index[case.get('id')] = index
        chart_id_list.append(case.get('id'))

    for insurance_index, customer_insurance in enumerate(insurance_list):
        if customer_insurance.monthly_premiums:
            monthly_premiums += customer_insurance.monthly_premiums
        if customer_insurance.monthly_renewal_premium:
            monthly_renewal_premium += customer_insurance.monthly_renewal_premium
        if customer_insurance.monthly_non_renewal_premium:
            monthly_non_renewal_premium += customer_insurance.monthly_non_renewal_premium

        if customer_insurance.monthly_earned_premium:
            if customer_insurance.insurance_type == 1 and customer_insurance.payment_period_type == 1:
                monthly_earned_premium += customer_insurance.monthly_earned_premium
            elif customer_insurance.insurance_type == 2:
                monthly_earned_premium += customer_insurance.monthly_earned_premium

        if customer_insurance.total_premiums:
            total_premiums += customer_insurance.total_premiums

        if customer_insurance.total_renewal_premium:
            total_renewal_premium += customer_insurance.total_renewal_premium

        if customer_insurance.total_non_renewal_premium:
            total_non_renewal_premium += customer_insurance.total_non_renewal_premium

        if customer_insurance.total_earned_premium:
            total_earned_premium += customer_insurance.total_earned_premium

        # 기납회차 : 계약일, 확인일 Month
        # prepaid_months = 0
        # 기납보험료 : 기납 회차 * 월 보험료
        # prepaid_insurance_premium = prepaid_months * customer_insurance.monthly_premiums
        # 남은회차 아직 필요없음
        # pay_insurance_premium = total_premiums - prepaid_insurance_premium  # 낼 돈

        now_date = datetime.datetime.now()
        birth_day_date = None
        prepaid_months = 0
        # 기납회차 : 계약일, 확인일 Month
        if customer_insurance.old:
            start_old = customer_insurance.old
        else:
            contract_date = datetime.datetime.strptime(customer_insurance.contract_date, '%Y.%m.%d')
            r = relativedelta(now_date, contract_date)
            prepaid_months = r.years * 12 + r.months

            if customer_insurance.payment_period_type == 1:
                if prepaid_months > customer_insurance.non_renewal_month:
                    prepaid_months = customer_insurance.non_renewal_month

            birth_day_date = datetime.datetime.strptime(birth_day, '%Y.%m.%d')
            old_date = relativedelta(now_date, birth_day_date)
            old = old_date.years + 1
            start_old = old
            contract_old = old - (now_date.year - contract_date.year)

        # 기납보험료 : 기납 회차 * 월 보험료
        prepaid_insurance_premium = prepaid_months * customer_insurance.monthly_premiums  # 낸 돈
        # 남은회차 아직 필요없음
        pay_insurance_premium = total_premiums - prepaid_insurance_premium  # 낼 돈

        total_prepaid_insurance_premium = total_prepaid_insurance_premium + prepaid_insurance_premium
        total_pay_insurance_premium = total_pay_insurance_premium + pay_insurance_premium

        # 환급금
        cancellation_refund = 0
        if customer_insurance.cancellation_refund:
            cancellation_refund = customer_insurance.cancellation_refund

        # 환급 손실금 : 기납 보험료 - 혜약환급금
        cancellation_loss = prepaid_insurance_premium - cancellation_refund
        total_cancellation_refund = total_cancellation_refund + cancellation_refund
        total_cancellation_loss = total_cancellation_loss + cancellation_loss

        customer_insurance_case_list = customer_insurance.case_list.all()
        for case in customer_insurance_case_list:
            index = case_list_index[case.detail.id]

            if case.payment_period_type == 1 or case.payment_period_type == 2:
                case_list[index]['total_non_renewal_premium'] += case.assurance_amount
            if case.payment_period_type == 3:
                case_list[index]['total_renewal_premium'] += case.assurance_amount

            case_list[index]['total_premium'] = case_list[index]['total_renewal_premium'] + case_list[index][
                'total_non_renewal_premium']

            case_list[index]['total_premium_list'][insurance_index] = case.assurance_amount

            if case.warranty_period_type < 4 and not case.warranty_period:
                continue

            case_list[index]['is_show_old_price'] = True

            if case.warranty_period_type == 2:  # 년 인경우
                end_old = contract_old + int(case.warranty_period)
            if case.warranty_period_type == 1:  # 세 인경우
                end_old = int(case.warranty_period)
                if end_old > 100:
                    end_old = 100
            if case.warranty_period_type == 3:  # 날짜
                case_warranty_period = str(case.warranty_period)
                if len(case_warranty_period) == 8:
                    warranty_period_date = datetime.datetime.strptime(case.warranty_period, '%Y%m%d')
                else:
                    warranty_period_date = datetime.datetime.strptime(case.warranty_period, '%Y.%m.%d')

                if birth_day_date:
                    end_old = warranty_period_date.year - birth_day_date.year
                else:
                    end_old = start_old + warranty_period_date.year - now_date.year

            if case.warranty_period_type == 4:  # 종신
                end_old = 100

            for old_index in range(0, 10):
                old_length_start = (old_index * 10)  # 나이 구간 시작
                old_length_end = (old_index * 10) + 10  # 나이 구간 끝

                # 가입 < end and start < 만기 (15 < 10 and 0 < 45)
                if start_old < old_length_end and old_length_start < end_old:
                    if case.payment_period_type == 1 or case.payment_period_type == 2:
                        case_list[index]['non_renewal_old_list'][old_index] += case.assurance_amount
                    if case.payment_period_type == 3:
                        case_list[index]['renewal_old_list'][old_index] += case.assurance_amount

            chart_detail_id_list = list(case.detail.chart_detail.values_list('id', flat=True))
            if case.detail.name == '일반사망':
                chart_detail_id_list = [1]
            if case.detail.name == '재해사망':
                chart_detail_id_list = [2]

            for chart_id in chart_detail_id_list:
                if chart_id not in chart_id_list:
                    continue

                index = chart_list_index[chart_id]

                if case.payment_period_type == 1 or case.payment_period_type == 2:
                    chart_list[index]['total_non_renewal_premium'] += case.assurance_amount
                    # total_non_renewal_premium = case.assurance_amount
                if case.payment_period_type == 3:
                    chart_list[index]['total_renewal_premium'] += case.assurance_amount

                chart_list[index]['total_premium'] = chart_list[index]['total_renewal_premium'] + chart_list[index][
                    'total_non_renewal_premium']


    result = {
        'insurance_list': CustomerInsuranceSerializer(insurance_list, many=True).data,  # 기본정보
        'monthly_premiums': monthly_premiums,
        'monthly_renewal_premium': monthly_renewal_premium,
        'monthly_non_renewal_premium': monthly_non_renewal_premium,
        'monthly_earned_premium': monthly_earned_premium,
        'total_premiums': total_premiums,
        'total_renewal_premium': total_renewal_premium,
        'total_non_renewal_premium': total_non_renewal_premium,
        'total_earned_premium': total_earned_premium,
        'total_cancellation_refund': total_cancellation_refund,
        'total_cancellation_loss': total_cancellation_loss,
        'total_prepaid_insurance_premium': total_prepaid_insurance_premium,
        'total_pay_insurance_premium': total_pay_insurance_premium,
        'case_list': case_list,
        'chart_list': chart_list,
    }

    return result



def calculate_total_analysis(birth_day, case_list, chart_list, insurance_list):
    monthly_premiums = 0  # 월 납입 보험료
    monthly_renewal_premium = 0  # 월 갱신 보험료
    monthly_non_renewal_premium = 0  # 월 비갱신 보험료
    monthly_earned_premium = 0  # 월 적립 보험료
    total_premiums = 0  # 총 보험료
    total_renewal_premium = 0  # 총 갱신 보험료
    total_non_renewal_premium = 0  # 총 비갱신 보험료
    total_earned_premium = 0  # 총 적립 보험료
    total_cancellation_refund = 0  # 총 환급금
    total_cancellation_loss = 0  # 총 손실금
    total_prepaid_insurance_premium = 0
    total_pay_insurance_premium = 0

    case_list_index = {}
    case_id_list = []
    chart_list_index = {}
    chart_id_list = []

    for index, case in enumerate(case_list):
        case['total_premium'] = 0
        case['total_renewal_premium'] = 0
        case['total_non_renewal_premium'] = 0
        case['non_renewal_old_list'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 무조건 10개
        case['renewal_old_list'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 무조건 10개
        case['total_premium_list'] = [0] * len(insurance_list)
        case['is_show_old_price'] = False
        case_list_index[case.get('id')] = index
        case_id_list.append(case.get('id'))

    for index, case in enumerate(chart_list):
        case['total_premium'] = 0
        case['total_renewal_premium'] = 0
        case['total_non_renewal_premium'] = 0
        chart_list_index[case.get('id')] = index
        chart_id_list.append(case.get('id'))


    for insurance_index, customer_insurance in enumerate(insurance_list):
        if customer_insurance.monthly_premiums:
            monthly_premiums += customer_insurance.monthly_premiums
        if customer_insurance.monthly_renewal_premium:
            monthly_renewal_premium += customer_insurance.monthly_renewal_premium
        if customer_insurance.monthly_non_renewal_premium:
            monthly_non_renewal_premium += customer_insurance.monthly_non_renewal_premium

        if customer_insurance.monthly_earned_premium:
            if customer_insurance.insurance_type == 1 and customer_insurance.payment_period_type == 1:
                monthly_earned_premium += customer_insurance.monthly_earned_premium
            elif customer_insurance.insurance_type == 2:
                monthly_earned_premium += customer_insurance.monthly_earned_premium

        if customer_insurance.total_premiums:
            total_premiums += customer_insurance.total_premiums

        if customer_insurance.total_renewal_premium:
            total_renewal_premium += customer_insurance.total_renewal_premium

        if customer_insurance.total_non_renewal_premium:
            total_non_renewal_premium += customer_insurance.total_non_renewal_premium

        if customer_insurance.total_earned_premium:
            total_earned_premium += customer_insurance.total_earned_premium

        now_date = datetime.datetime.now()
        prepaid_months = 0
        # 기납회차 : 계약일, 확인일 Month
        if customer_insurance.old:
            contract_old = customer_insurance.old
            start_old = customer_insurance.old
        else:
            contract_date = datetime.datetime.strptime(customer_insurance.contract_date, '%Y.%m.%d')
            r = relativedelta(now_date, contract_date)
            prepaid_months = r.years * 12 + r.months

            if customer_insurance.payment_period_type == 1:
                if prepaid_months > customer_insurance.non_renewal_month:
                    prepaid_months = customer_insurance.non_renewal_month

            birth_day_date = datetime.datetime.strptime(birth_day, '%Y.%m.%d')
            old_date = relativedelta(now_date, birth_day_date)
            old = old_date.years + 1
            start_old = old
            contract_old = old - (now_date.year - contract_date.year)

        # 기납보험료 : 기납 회차 * 월 보험료
        prepaid_insurance_premium = prepaid_months * customer_insurance.monthly_premiums  # 낸 돈
        # 남은회차 아직 필요없음
        pay_insurance_premium = customer_insurance.total_premiums - prepaid_insurance_premium  # 낼 돈

        total_prepaid_insurance_premium = total_prepaid_insurance_premium + prepaid_insurance_premium
        total_pay_insurance_premium = total_pay_insurance_premium + pay_insurance_premium
        # 환급금
        cancellation_refund = 0
        if customer_insurance.cancellation_refund:
            cancellation_refund = customer_insurance.cancellation_refund

        # 환급 손실금 : 기납 보험료 - 혜약환급금
        cancellation_loss = prepaid_insurance_premium - cancellation_refund
        total_cancellation_refund = total_cancellation_refund + cancellation_refund
        total_cancellation_loss = total_cancellation_loss + cancellation_loss

        customer_insurance_case_list = customer_insurance.case_list.all()

        for case in customer_insurance_case_list:
            analysis_detail_id_list = list(case.detail.analysis_detail.values_list('id', flat=True))
            for analysis_id in analysis_detail_id_list:
                if analysis_id not in case_id_list:
                    continue

                index = case_list_index[analysis_id]

                if case.payment_period_type == 1 or case.payment_period_type == 2:
                    case_list[index]['total_non_renewal_premium'] += case.assurance_amount
                if case.payment_period_type == 3:
                    case_list[index]['total_renewal_premium'] += case.assurance_amount

                case_list[index]['total_premium'] = case_list[index]['total_renewal_premium'] + case_list[index][
                    'total_non_renewal_premium']

                case_list[index]['total_premium_list'][insurance_index] = case.assurance_amount

                if case.warranty_period_type < 4 and not case.warranty_period:
                    continue

                case_list[index]['is_show_old_price'] = True

                if case.warranty_period_type == 2:  # 년 인경우
                    end_old = contract_old + int(case.warranty_period)
                if case.warranty_period_type == 1:  # 세 인경우
                    end_old = int(case.warranty_period)
                    if end_old > 100:
                        end_old = 100
                if case.warranty_period_type == 3:  # 날짜
                    case_warranty_period = str(case.warranty_period)
                    if len(case_warranty_period) == 8:
                        warranty_period_date = datetime.datetime.strptime(case.warranty_period, '%Y%m%d')
                    else:
                        warranty_period_date = datetime.datetime.strptime(case.warranty_period, '%Y.%m.%d')

                    if birth_day_date:
                        end_old = warranty_period_date.year - birth_day_date.year
                    else:
                        end_old = start_old + warranty_period_date.year - now_date.year

                if case.warranty_period_type == 4:  # 종신
                    end_old = 100

                for old_index in range(0, 10):
                    old_length_start = (old_index * 10)  # 나이 구간 시작
                    old_length_end = (old_index * 10) + 10  # 나이 구간 끝

                    # 가입 < end and start < 만기 (15 < 10 and 0 < 45)
                    if start_old < old_length_end and old_length_start < end_old:
                        if case.payment_period_type == 1 or case.payment_period_type == 2:
                            case_list[index]['non_renewal_old_list'][old_index] += case.assurance_amount
                        if case.payment_period_type == 3:
                            case_list[index]['renewal_old_list'][old_index] += case.assurance_amount

            chart_detail_id_list = list(case.detail.chart_detail.values_list('id', flat=True))
            for chart_id in chart_detail_id_list:
                if chart_id not in chart_id_list:
                    continue

                index = chart_list_index[chart_id]

                if case.payment_period_type == 1 or case.payment_period_type == 2:
                    chart_list[index]['total_non_renewal_premium'] += case.assurance_amount
                    # total_non_renewal_premium = case.assurance_amount
                if case.payment_period_type == 3:
                    chart_list[index]['total_renewal_premium'] += case.assurance_amount

                chart_list[index]['total_premium'] = chart_list[index]['total_renewal_premium'] + chart_list[index][
                    'total_non_renewal_premium']

    result = {
        'insurance_list': CustomerInsuranceSerializer(insurance_list, many=True).data,  # 기본정보
        'monthly_premiums': monthly_premiums,
        'monthly_renewal_premium': monthly_renewal_premium,
        'monthly_non_renewal_premium': monthly_non_renewal_premium,
        'monthly_earned_premium': monthly_earned_premium,
        'total_premiums': total_premiums,
        'total_renewal_premium': total_renewal_premium,
        'total_non_renewal_premium': total_non_renewal_premium,
        'total_earned_premium': total_earned_premium,
        'total_cancellation_refund': total_cancellation_refund,
        'total_cancellation_loss': total_cancellation_loss,
        'total_prepaid_insurance_premium': total_prepaid_insurance_premium,
        'total_pay_insurance_premium': total_pay_insurance_premium,
        'case_list': case_list,
        'chart_list': chart_list,
    }

    return result

