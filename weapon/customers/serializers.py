from rest_framework import serializers
from .models import Customer, CustomerMedicalHistory, CustomerGroup


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerSerializerForDetail(serializers.ModelSerializer):
    parent_customer = serializers.SerializerMethodField()
    group_customers = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = "__all__"

    def get_parent_customer(self, instance):
        parent_customer = instance.parent_customers.all().first()
        if parent_customer:
            return CustomerSerializer(parent_customer.parent_customer).data
        return None

    def get_parent_customer_id(self, instance):
        parent_customer = instance.parent_customers.all().first()
        if parent_customer:
            return parent_customer.parent_customer.id
        return None

    def get_group_customers(self, instance):
        return instance.child_customers.all().values_list('child_customer', flat=True)


class CustomerSerializerWithInsuranceCount(serializers.ModelSerializer):
    insurance_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ("id", "name", "insurance_count",)

    def get_insurance_count(self, instance):
        return len(instance.customer_insurance_list.filter(portfolio_type=1))


class CustomerMedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMedicalHistory
        fields = "__all__"


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = "__all__"


class CustomerGroupSerializerWithInsuranceCount(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    birth_day = serializers.SerializerMethodField()
    insurance_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomerGroup
        fields = ("id", "customer", "name", "birth_day", "insurance_count",)

    def get_name(self, instance):
        return instance.child_customer.name

    def get_birth_day(self, instance):
        return instance.child_customer.birth_day

    def get_customer(self, instance):
        return instance.child_customer.id

    def get_insurance_count(self, instance):
        return len(instance.child_customer.customer_insurance_list.all())
