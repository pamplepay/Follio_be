from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from weapon.insurances.models import InsuranceCategory, InsuranceSubCategory, InsuranceDetail, Insurance, \
    AnalysisSubCategory, AnalysisDetail, ChartDetail

User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):

        analysis_sub_category = AnalysisSubCategory.objects.get(name='운전자')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '변호사 선임비'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()

        chart_detail = ChartDetail()
        chart_detail.name = '상해사망'
        chart_detail.chart_based_amount = 15000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '질병사망'
        chart_detail.chart_based_amount = 15000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '상해 후유장애'
        chart_detail.chart_based_amount = 15000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '암'
        chart_detail.chart_based_amount = 4000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '뇌'
        chart_detail.chart_based_amount = 5000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '심장'
        chart_detail.chart_based_amount = 3000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '배상책임'
        chart_detail.chart_based_amount = 10000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '형사합의 실손비'
        chart_detail.insurance_type = 2
        chart_detail.chart_based_amount = 10000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '대인 벌금'
        chart_detail.insurance_type = 2
        chart_detail.chart_based_amount = 2000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '대물 벌금'
        chart_detail.insurance_type = 2
        chart_detail.chart_based_amount = 500
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '변호사 선임비'
        chart_detail.chart_based_amount = 2000
        chart_detail.insurance_type = 2
        chart_detail.save()
        
        chart_detail = ChartDetail()
        chart_detail.name = '상해 입원 의료비'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 5000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '상해 통원 의료비'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 50
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '질병 입원 의료비'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 5000
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '질병 통원 의료비'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 30
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '비급여 도수치료 등'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 350
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '비급여 MRI/MRA'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 300
        chart_detail.save()
        chart_detail = ChartDetail()
        chart_detail.name = '비급여 주사료'
        chart_detail.chart_type = 2
        chart_detail.chart_based_amount = 250
        chart_detail.save()
        
        analysis_sub_category = AnalysisSubCategory.objects.get(name='사망')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '상해사망'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '질병사망'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_sub_category = AnalysisSubCategory.objects.get(name='후유장애')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '상해후유장애 3~100%(재해상해)'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_sub_category = AnalysisSubCategory.objects.get(name='암')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '일반암'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '유사암'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        
        analysis_sub_category = AnalysisSubCategory.objects.get(name='뇌')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '뇌혈관'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '뇌졸중'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '뇌출혈'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        
        analysis_sub_category = AnalysisSubCategory.objects.get(name='심장')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '혀혈성'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '급성심근경색'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '대인 벌금'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '대물 벌금'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '형사 합의 실손비'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        
        analysis_sub_category = AnalysisSubCategory.objects.get(name='기타')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '가족생활배상책임'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '일반생활배상책임'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        
        analysis_sub_category = AnalysisSubCategory.objects.get(name='상해')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '상해 입원 의료비'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '상해 통원 의료비'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_sub_category = AnalysisSubCategory.objects.get(name='질병')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '질병 입원 의료비'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '질병 통원 의료비'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_sub_category = AnalysisSubCategory.objects.get(name='비급여')
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '비급여 도수치료 등'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '비급여 MRI/MRA'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()
        analysis_detail = AnalysisDetail()
        analysis_detail.name = '비급여 주사료'
        analysis_detail.sub_category = analysis_sub_category
        analysis_detail.save()

        # category_list = [];
        # category_list.append(Category(name='호이'))
        Insurance.objects.create(name='한화손해')
        Insurance.objects.create(name='메리츠화재')
        Insurance.objects.create(name='현대해상')
        Insurance.objects.create(name='KB손해')
        Insurance.objects.create(name='DB손해')
        Insurance.objects.create(name='삼성화재')
        Insurance.objects.create(name='MG손해')
        Insurance.objects.create(name='NH농협손해')
        Insurance.objects.create(name='우체국보험')
        Insurance.objects.create(name='흥국화재')
        Insurance.objects.create(name='롯데손해')
        Insurance.objects.create(name='AIG손해')
        Insurance.objects.create(name='AXA손해')
        Insurance.objects.create(name='에이스손해')
        Insurance.objects.create(name='하나손해')
        Insurance.objects.create(name='한화생명')
        Insurance.objects.create(name='삼성생명')
        Insurance.objects.create(name='DB생명')
        Insurance.objects.create(name='신한생명')
        Insurance.objects.create(name='하나생명')
        Insurance.objects.create(name='KB생명')
        Insurance.objects.create(name='흥국생명')
        Insurance.objects.create(name='교보생명')
        Insurance.objects.create(name='NH농협생명')
        Insurance.objects.create(name='푸본현대생명')
        Insurance.objects.create(name='교보라이프플래닛')
        Insurance.objects.create(name='동양생명')
        Insurance.objects.create(name='KDB생명')
        Insurance.objects.create(name='미레에셋생명')
        Insurance.objects.create(name='DGB생명')
        Insurance.objects.create(name='ABL생명')
        Insurance.objects.create(name='메트라이프생명')
        Insurance.objects.create(name='푸르덴셜생명')
        Insurance.objects.create(name='처브라이프생명')
        Insurance.objects.create(name='오렌지라이프생명')
        Insurance.objects.create(name='라이나생명')
        Insurance.objects.create(name='BNP파리바카디프생명')
        Insurance.objects.create(name='AIA생명')

        detail_list = InsuranceDetail.objects.all()
        for detail in detail_list:
            if detail.name == '일반사망' or detail.name == '상해사망' or detail.name == '질병사망' or detail.name == '재해사망' or detail.name == '상해후유장애':
                detail.chart_based_amount = 15000
            if detail.name == '일반암' or detail.name == '유사암' or detail.name == '뇌졸중' or detail.name == '뇌출혈' or detail.name == '급성심근경색' or detail.name == '변호사 선임비' or detail.name == '대인 벌금':
                detail.chart_based_amount = 2000
            if detail.name == '뇌혈관' or detail.name == '허혈성':
                detail.chart_based_amount = 1000
            if detail.name == '대물 벌금':
                detail.chart_based_amount = 500
            if detail.name == '형사 합의 실손비' or detail.name == '가족생활배상책임' or detail.name == '일상생활배상책임':
                detail.chart_based_amount = 10000
        
            if detail.name == '상해 입원 의료비' or detail.name == '질병 입원 의료비':
                detail.chart_based_amount = 5000
                detail.chart_type = 2
            if detail.name == '상해 통원 의료비' or detail.name == '질병 통원 의료비':
                detail.chart_based_amount = 30
                detail.chart_type = 2
            if detail.name == '비급여 도수치료 등':
                detail.chart_based_amount = 350
                detail.chart_type = 2
            if detail.name == '비급여 MR/MRA':
                detail.chart_based_amount = 300
                detail.chart_type = 2
            if detail.name == '비급여 주사료':
                detail.chart_based_amount = 250
                detail.chart_type = 2

            detail.save()
            # 실손 의료비
            # category = InsuranceCategory.objects.create(name='실손 의료비')
            # sub_category = InsuranceSubCategory.objects.create(category=category, name='상해')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='상해 입원 의료비')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='상해 통원 의료비')
            # sub_category = InsuranceSubCategory.objects.create(category=category, name='질병')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='질병 입원 의료비')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='질병 통원 의료비')
            # sub_category = InsuranceSubCategory.objects.create(category=category, name='비급여')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='비급여 도수치료 등')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='비급여 MR/MRA')
            # InsuranceDetail.objects.create(sub_category=sub_category, name='비급여 주사료')
            print('Done!')
        # 일반사망	15,000
        # 상해사망	15,000
        # 질병사망	15,000
        # 재해사망	15,000
        # 상해후유장애	15,000
        # "재해 상해 3~100%"
        # 일반암	2,000
        # 유사암	2,000
        # 뇌혈관	1,000
        # 뇌졸중	2,000
        # 뇌출혈	2,000
        # 허혈성	1,000

        # 급성심근경색	2,000
        # 변호사 선임비	2,000
        # 대물 벌금	500
        # 대인 벌금	2,000
        # 형사합의 실손비	10,000
        # 배상책임	10,000

        # 상해 입원	5,000
        # 상해 통원	30
        # 질병 입원	5,000
        # 질병 통원	30
        # 비급여 도수치료 등	350
        # 비급여 MRI/MRA	300
        # 비급여 주사료	250

        # 100 %면 글씨 색상 변경

        with transaction.atomic():
            # 사망
            category = InsuranceCategory.objects.create(name='사망')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='일반', insurance_type=1)
            InsuranceDetail.objects.create(sub_category=sub_category, name='일반사망')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='재해', insurance_type=1)
            InsuranceDetail.objects.create(sub_category=sub_category, name='재해사망')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='상해', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='상해사망')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='질병', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='질병사망')
        
            # 재해
            category = InsuranceCategory.objects.create(name="재해", insurance_type=1)
            sub_category = InsuranceSubCategory.objects.create(category=category, name='상해', insurance_type=1)
            InsuranceDetail.objects.create(sub_category=sub_category, name='재해 상해 3~100%')
        
            # 상해
            category = InsuranceCategory.objects.create(name='상해', insurance_type=2)
            sub_category = InsuranceSubCategory.objects.create(category=category, name='상해', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='상해후유장애 3~100%')
        
            # 진단비
            category = InsuranceCategory.objects.create(name='진단비')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='암')
            InsuranceDetail.objects.create(sub_category=sub_category, name='일반암')
            InsuranceDetail.objects.create(sub_category=sub_category, name='유사암')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='뇌')
            InsuranceDetail.objects.create(sub_category=sub_category, name='뇌혈관')
            InsuranceDetail.objects.create(sub_category=sub_category, name='뇌졸중')
            InsuranceDetail.objects.create(sub_category=sub_category, name='뇌출혈')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='심혈관')
            InsuranceDetail.objects.create(sub_category=sub_category, name='허혈성')
            InsuranceDetail.objects.create(sub_category=sub_category, name='급성심근경색')
        
            # 운전자
            category = InsuranceCategory.objects.create(name='진단비', insurance_type=2)
            sub_category = InsuranceSubCategory.objects.create(category=category, name='변호사', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='변호사 선임비')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='벌금', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='대물 벌금')
            InsuranceDetail.objects.create(sub_category=sub_category, name='대인 벌금')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='합의금', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='형사 합의 실손비')
        
            # 기타
            category = InsuranceCategory.objects.create(name='기타', insurance_type=2)
            sub_category = InsuranceSubCategory.objects.create(category=category, name='가족', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='가족생활배상책임')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='일상', insurance_type=2)
            InsuranceDetail.objects.create(sub_category=sub_category, name='일상생활배상책임')
        
            # 실손 의료비
            category = InsuranceCategory.objects.create(name='실손 의료비')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='상해')
            InsuranceDetail.objects.create(sub_category=sub_category, name='상해 입원 의료비')
            InsuranceDetail.objects.create(sub_category=sub_category, name='상해 통원 의료비')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='질병')
            InsuranceDetail.objects.create(sub_category=sub_category, name='질병 입원 의료비')
            InsuranceDetail.objects.create(sub_category=sub_category, name='질병 통원 의료비')
            sub_category = InsuranceSubCategory.objects.create(category=category, name='비급여')
            InsuranceDetail.objects.create(sub_category=sub_category, name='비급여 도수치료 등')
            InsuranceDetail.objects.create(sub_category=sub_category, name='비급여 MR/MRA')
            InsuranceDetail.objects.create(sub_category=sub_category, name='비급여 주사료')
        print('Done!')
        pass

