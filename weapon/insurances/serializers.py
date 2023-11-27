from rest_framework import serializers

from weapon.insurances.models import CustomerInsurance, InsuranceCategory, InsuranceSubCategory, \
    InsuranceDetail, Insurance, InsuranceTag, CustomerInsuranceDetail, AnalysisCategory, AnalysisSubCategory, \
    AnalysisDetail


class InsuranceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceTag
        fields = "__all__"


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = "__all__"


class CustomerInsuranceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="insurance.image", read_only=True)
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomerInsurance
        fields = "__all__"

    def get_customer_name(self, instance):
        if instance.customer:
            return instance.customer.name
        return None


class CustomerInsuranceSerializerForDetail(serializers.ModelSerializer):
    image = serializers.ImageField(source="insurance.image", read_only=True)
    case_list = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomerInsurance
        fields = "__all__"

    def get_case_list(self, instance):
        case_list = instance.case_list.all()
        return CustomerInsuranceDetailSerializer(case_list, many=True).data

    def get_customer_name(self, instance):
        if instance.customer:
            return instance.customer.name
        return None


class InsuranceCategorySerializer(serializers.ModelSerializer):
    sub_category_list = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceCategory
        fields = "__all__"

    def get_sub_category_list(self, instance):
        sub_category_list = instance.sub_categories.all()
        return InsuranceSubCategorySerializer(sub_category_list, many=True).data


class InsuranceSubCategorySerializer(serializers.ModelSerializer):
    detail_list = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceSubCategory
        fields = "__all__"

    def get_detail_list(self, instance):
        detail_list = instance.details.all()
        return InsuranceDetailSerializer(detail_list, many=True).data


class InsuranceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceDetail
        fields = "__all__"


class CustomerInsuranceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInsuranceDetail
        fields = "__all__"


class AnalysisCategorySerializer(serializers.ModelSerializer):
    sub_category_list = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisCategory
        fields = "__all__"

    def get_sub_category_list(self, instance):
        sub_category_list = instance.sub_categories.all()
        return AnalysisSubCategorySerializer(sub_category_list, many=True).data


class AnalysisSubCategorySerializer(serializers.ModelSerializer):
    detail_list = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisSubCategory
        fields = "__all__"

    def get_detail_list(self, instance):
        detail_list = instance.details.all()
        return AnalysisDetailSerializer(detail_list, many=True).data


class AnalysisDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisDetail
        fields = "__all__"

