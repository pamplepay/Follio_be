from django.contrib import admin

from weapon.insurances.models import InsuranceTag, Insurance, InsuranceCategory, InsuranceSubCategory, InsuranceDetail, \
    AnalysisCategory, AnalysisSubCategory, AnalysisDetail, ChartDetail, CustomerInsurance


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('name', 'insurance_type')


@admin.register(InsuranceTag)
class InsuranceTagAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(InsuranceCategory)
class InsuranceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(InsuranceSubCategory)
class InsuranceSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(InsuranceDetail)
class InsuranceDetailAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AnalysisCategory)
class AnalysisCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(AnalysisSubCategory)
class AnalysisSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AnalysisDetail)
class AnalysisDetailAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ChartDetail)
class ChartDetailAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CustomerInsurance)
class CustomerInsuranceAdmin(admin.ModelAdmin):
    list_display = ('id', 'portfolio_type', 'is_common', 'user', 'customer', 'contractor_name', 'insured_name')

